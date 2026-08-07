from flask import Blueprint, render_template, request, redirect, url_for, session
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
        role = request.form.get('role')
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter(User.username.ilike(username)).first()

        if user and (check_password_hash(user.password_hash, password) or user.password_hash == password):
            session['user_id'] = user.user_id
            session['username'] = user.username
            session['role'] = user.role.lower()

            user_role = user.role.lower()
            if user_role == 'admin':
                return redirect(url_for('admin.dashboard'))
            elif user_role in ['branch', 'branch_admin', 'branch admin']:
                return redirect(url_for('admin.branches'))
            elif user_role == 'faculty':
                return redirect(url_for('admin.faculty'))
            elif user_role == 'student':
                return redirect(url_for('student.dashboard'))
        
        return render_template('login.html', error="Invalid Credentials or Role")

    return render_template('login.html')

@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))