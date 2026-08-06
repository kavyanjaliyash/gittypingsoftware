from flask import Blueprint, render_template, session, redirect, url_for, request
from database import db
from models import Student, Course, Lesson, Screen, User
import unicodedata

student_bp = Blueprint('student', __name__, url_prefix='/student')

@student_bp.route('/dashboard')
def dashboard():
    if 'user_id' not in session or session.get('role') != 'student':
        return redirect(url_for('auth.login'))
    
    student = Student.query.filter_by(user_id=session['user_id']).first()
    courses = Course.query.filter_by(status='Active').all()
    
    return render_template('student/dashboard.html', student=student, courses=courses)

@student_bp.route("/courses")
def student_courses():
    if "username" not in session:
        return redirect(url_for('auth.login'))

    user = User.query.filter_by(username=session["username"]).first()
    student = Student.query.filter_by(user_id=user.user_id).first()
    courses = Course.query.filter_by(status="Active").all()

    return render_template(
        "student/courses.html",
        student=student,
        courses=courses
    )

@student_bp.route("/course/<int:course_id>")
def student_course(course_id):
    if 'user_id' not in session or session.get('role') != 'student':
        return redirect(url_for('auth.login'))
        
    student = Student.query.filter_by(user_id=session['user_id']).first()
    course = Course.query.get_or_404(course_id)
    lessons = Lesson.query.filter_by(
        course_id=course_id,
        status="Active"
    ).order_by(Lesson.display_order).all()

    return render_template(
        "student/course_lessons.html",
        student=student,
        course=course,
        lessons=lessons
    )

@student_bp.route('/lesson/<int:lesson_id>')
def student_lesson(lesson_id):
    if 'user_id' not in session or session.get('role') != 'student':
        return redirect(url_for('auth.login'))
    
    student = Student.query.filter_by(user_id=session['user_id']).first()
    lesson = Lesson.query.get_or_404(lesson_id)
    screens = Screen.query.filter_by(lesson_id=lesson_id).all()
    
    return render_template(
        'student/lesson.html', 
        student=student, 
        lesson=lesson, 
        screens=screens
    )

@student_bp.route('/lesson/<int:lesson_id>/complete', methods=['POST'])
def complete_lesson(lesson_id):
    if 'user_id' not in session or session.get('role') != 'student':
        return redirect(url_for('auth.login'))
    
    student = Student.query.filter_by(user_id=session['user_id']).first()
    lesson = Lesson.query.get_or_404(lesson_id)
    
    wpm = request.form.get('wpm', 0)
    mistakes = request.form.get('mistakes', 0)
    seconds = request.form.get('seconds', 0)
    
    next_lesson = Lesson.query.filter(
        Lesson.course_id == lesson.course_id, 
        Lesson.display_order > lesson.display_order
    ).order_by(Lesson.display_order.asc()).first()
    
    return render_template(
        'student/completion.html', 
        student=student, 
        lesson=lesson, 
        wpm=wpm, 
        mistakes=mistakes, 
        seconds=seconds, 
        next_lesson=next_lesson
    )