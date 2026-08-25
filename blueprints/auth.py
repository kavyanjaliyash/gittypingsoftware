from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from database import db
from models import User
from werkzeug.security import check_password_hash

auth_bp = Blueprint('auth', __name__)

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