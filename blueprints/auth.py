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
                return render_template('login.html')

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
        return render_template('login.html')

    return render_template('login.html')

@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))