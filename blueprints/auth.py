import secrets
import hashlib
import os
from datetime import datetime, timedelta
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from database import db
from models import User, Branch, Faculty, PasswordResetOTP, Student
from werkzeug.security import check_password_hash, generate_password_hash
from utils.sms import send_otp_sms, mask_mobile, normalize_mobile

auth_bp = Blueprint('auth', __name__)

def get_user_mobile(user):
    """
    Resolves the registered mobile number for a User object (Admin, Branch, or Faculty).
    Returns normalized 10-digit mobile number string or None.
    """
    if not user:
        return None

    role = (user.role or '').strip().lower()

    # 1. Faculty Role -> Check Faculty table
    if role == 'faculty':
        fac = Faculty.query.filter_by(user_id=user.user_id).first()
        if fac and fac.mobile:
            return normalize_mobile(fac.mobile)

    # 2. Branch Role -> Check Branch table
    elif role in ['branch', 'branch_admin', 'branch admin']:
        br = Branch.query.filter_by(user_id=user.user_id).first()
        if br and br.phone:
            return normalize_mobile(br.phone)

    # 3. Admin Role -> Check linked Branch, Admin Branch ('Admin01'), or ADMIN_MOBILE_NUMBER env var
    elif role == 'admin':
        # Check linked Branch
        br = Branch.query.filter_by(user_id=user.user_id).first()
        if br and br.phone and normalize_mobile(br.phone):
            return normalize_mobile(br.phone)

        # Check Admin Branch ('Admin01')
        admin_br = Branch.query.filter_by(branch_code='Admin01').first()
        if admin_br and admin_br.phone and normalize_mobile(admin_br.phone):
            return normalize_mobile(admin_br.phone)

        # Fallback to env var
        env_admin_mobile = os.environ.get('ADMIN_MOBILE_NUMBER')
        if env_admin_mobile:
            return normalize_mobile(env_admin_mobile)

    return None

@auth_bp.route('/')
def index():
    return redirect(url_for('auth.login'))

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        role = request.form.get('role', '').strip().lower()
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()

        user = User.query.filter(User.username.ilike(username)).first()

        if user and (check_password_hash(user.password_hash, password) or user.password_hash == password):
            # Verify role matches
            db_role = user.role.lower()
            if role and role not in db_role and db_role not in role:
                flash("Selected role does not match account credentials", "danger")
                return render_template('login.html', selected_role=role)

            # Store role-scoped session variables to support concurrent logins in different tabs
            if db_role in ['branch', 'branch_admin', 'branch admin']:
                session['branch_user_id'] = user.user_id
                session['branch_username'] = user.username
            elif db_role == 'faculty':
                session['faculty_user_id'] = user.user_id
                session['faculty_username'] = user.username
            elif db_role == 'admin':
                session['admin_user_id'] = user.user_id
                session['admin_username'] = user.username
            elif db_role == 'student':
                session['student_user_id'] = user.user_id
                session['student_username'] = user.username

            # Also maintain active role & user_id for global references
            session['user_id'] = user.user_id
            session['username'] = user.username
            session['role'] = db_role

            if db_role == 'admin':
                return redirect(url_for('admin.dashboard'))
            elif db_role in ['branch', 'branch_admin', 'branch admin']:
                return redirect(url_for('branch.dashboard'))
            elif db_role == 'faculty':
                return redirect(url_for('faculty.dashboard'))
            elif db_role == 'student':
                return redirect(url_for('student.dashboard'))
        
        flash("Invalid Username or Password", "danger")
        return render_template('login.html', selected_role=role)

    role_param = request.args.get('role', '')
    return render_template('login.html', selected_role=role_param)

@auth_bp.route('/logout')
def logout():
    role = request.args.get('role', '').lower()
    if role == 'branch':
        session.pop('branch_user_id', None)
        session.pop('branch_username', None)
        if session.get('role') in ['branch', 'branch_admin', 'branch admin']:
            session.pop('user_id', None)
            session.pop('username', None)
            session.pop('role', None)
    elif role == 'faculty':
        session.pop('faculty_user_id', None)
        session.pop('faculty_username', None)
        if session.get('role') == 'faculty':
            session.pop('user_id', None)
            session.pop('username', None)
            session.pop('role', None)
    elif role == 'admin':
        session.pop('admin_user_id', None)
        session.pop('admin_username', None)
        if session.get('role') == 'admin':
            session.pop('user_id', None)
            session.pop('username', None)
            session.pop('role', None)
    elif role == 'student':
        session.pop('student_user_id', None)
        session.pop('student_username', None)
        if session.get('role') == 'student':
            session.pop('user_id', None)
            session.pop('username', None)
            session.pop('role', None)
    else:
        session.clear()
        
    return redirect(url_for('auth.login', role=role if role else None))

@auth_bp.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        generic_msg = "If the account exists and has a registered mobile number, a 6-digit OTP has been sent to your phone."

        if not username:
            flash("Please enter a valid username.", "danger")
            return render_template('forgot_password.html')

        user = User.query.filter(User.username.ilike(username)).first()

        # 1. Determine if user is a Student (role check + students table check)
        is_student = False
        if user:
            role_clean = (user.role or '').strip().lower()
            if role_clean == 'student' or Student.query.filter_by(user_id=user.user_id).first() is not None:
                is_student = True

        # STRICT EXCLUSION RULE: Students MUST NEVER enter the OTP flow (/verify-otp)
        if is_student:
            session.pop('reset_user_id', None)
            session.pop('reset_masked_mobile', None)
            session.pop('otp_verified_user_id', None)
            session.pop('otp_record_id', None)
            flash(generic_msg, "info")
            return render_template('forgot_password.html')

        # 2. Non-student accounts (Admin, Branch, Faculty)
        if not user or (user.status or '').strip().lower() != 'active':
            flash(generic_msg, "info")
            return redirect(url_for('auth.verify_otp'))

        # Check mobile number
        mobile = get_user_mobile(user)
        if not mobile:
            flash(generic_msg, "info")
            return redirect(url_for('auth.verify_otp'))

        # Rate Limiting: Max 3 OTP requests in 15 minutes
        fifteen_mins_ago = datetime.utcnow() - timedelta(minutes=15)
        recent_requests = PasswordResetOTP.query.filter(
            PasswordResetOTP.user_id == user.user_id,
            PasswordResetOTP.created_at >= fifteen_mins_ago
        ).count()

        if recent_requests >= 3:
            flash("Too many OTP requests. Please wait 15 minutes before trying again.", "warning")
            return render_template('forgot_password.html')

        # Generate 6-digit cryptographically secure OTP
        raw_otp = str(secrets.randbelow(900000) + 100000)
        otp_hash = hashlib.sha256(raw_otp.encode('utf-8')).hexdigest()
        expires_at = datetime.utcnow() + timedelta(minutes=10)

        # Invalidate previous unused OTPs for this user
        PasswordResetOTP.query.filter_by(user_id=user.user_id, used=False).update({'used': True})

        # Save new OTP record
        reset_otp = PasswordResetOTP(
            user_id=user.user_id,
            otp_hash=otp_hash,
            created_at=datetime.utcnow(),
            expires_at=expires_at,
            attempts=0,
            used=False
        )
        db.session.add(reset_otp)
        db.session.commit()

        # Send OTP SMS
        send_otp_sms(mobile, raw_otp)

        # Store reset context in session for verification
        session['reset_user_id'] = user.user_id
        session['reset_masked_mobile'] = mask_mobile(mobile)

        flash(generic_msg, "info")
        return redirect(url_for('auth.verify_otp'))

    return render_template('forgot_password.html')

@auth_bp.route('/verify-otp', methods=['GET', 'POST'])
def verify_otp():
    masked_mobile = session.get('reset_masked_mobile')
    user_id = session.get('reset_user_id')

    if request.method == 'POST':
        input_otp = request.form.get('otp', '').strip()

        if not user_id or not input_otp or len(input_otp) != 6:
            flash("Invalid session or OTP format. Please enter a 6-digit number.", "danger")
            return render_template('verify_otp.html', masked_mobile=masked_mobile)

        input_hash = hashlib.sha256(input_otp.encode('utf-8')).hexdigest()

        # Find active unused OTP record for this user
        otp_record = PasswordResetOTP.query.filter_by(
            user_id=user_id,
            used=False
        ).order_by(PasswordResetOTP.otp_id.desc()).first()

        if not otp_record:
            flash("No active OTP found. Please request a new OTP.", "danger")
            return redirect(url_for('auth.forgot_password'))

        # Check Expiry
        if datetime.utcnow() > otp_record.expires_at:
            otp_record.used = True
            db.session.commit()
            flash("OTP has expired. Please request a new one.", "danger")
            return redirect(url_for('auth.forgot_password'))

        # Check Max Attempts (Limit to 3 attempts)
        if otp_record.attempts >= 3:
            otp_record.used = True
            db.session.commit()
            flash("Maximum verification attempts exceeded. Please request a new OTP.", "danger")
            return redirect(url_for('auth.forgot_password'))

        # Verify OTP hash
        if otp_record.otp_hash != input_hash:
            otp_record.attempts += 1
            db.session.commit()
            remaining = 3 - otp_record.attempts
            if remaining > 0:
                flash(f"Incorrect OTP. {remaining} attempt(s) remaining.", "danger")
            else:
                otp_record.used = True
                db.session.commit()
                flash("Maximum verification attempts exceeded. Please request a new OTP.", "danger")
                return redirect(url_for('auth.forgot_password'))
            return render_template('verify_otp.html', masked_mobile=masked_mobile)

        # OTP Verified Successfully!
        session['otp_verified_user_id'] = user_id
        session['otp_record_id'] = otp_record.otp_id
        flash("OTP verified successfully. Please enter your new password.", "success")
        return redirect(url_for('auth.reset_password'))

    return render_template('verify_otp.html', masked_mobile=masked_mobile)

@auth_bp.route('/reset-password', methods=['GET', 'POST'])
def reset_password():
    user_id = session.get('otp_verified_user_id')
    otp_record_id = session.get('otp_record_id')

    if not user_id or not otp_record_id:
        flash("Unauthorized access or session expired. Please start again.", "danger")
        return redirect(url_for('auth.forgot_password'))

    if request.method == 'POST':
        new_password = request.form.get('new_password', '').strip()
        confirm_password = request.form.get('confirm_password', '').strip()

        if len(new_password) < 6:
            flash("Password must be at least 6 characters long.", "danger")
            return render_template('reset_password.html')

        if new_password != confirm_password:
            flash("Passwords do not match.", "danger")
            return render_template('reset_password.html')

        user = db.session.get(User, user_id)
        if not user or user.role.strip().lower() == 'student':
            flash("Account reset error.", "danger")
            return redirect(url_for('auth.login'))

        # Update password hash using Werkzeug generate_password_hash
        user.password_hash = generate_password_hash(new_password)

        # Consume / invalidate OTP immediately
        otp_rec = db.session.get(PasswordResetOTP, otp_record_id)
        if otp_rec:
            otp_rec.used = True

        db.session.commit()

        # Clear reset session tokens
        session.pop('reset_user_id', None)
        session.pop('reset_masked_mobile', None)
        session.pop('otp_verified_user_id', None)
        session.pop('otp_record_id', None)

        flash("Password reset successfully. Please log in with your new password.", "success")
        return redirect(url_for('auth.login'))

    return render_template('reset_password.html')