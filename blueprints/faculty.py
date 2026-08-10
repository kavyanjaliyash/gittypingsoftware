from flask import Blueprint, render_template, session, redirect, url_for, request, flash
from database import db
from models import User, Faculty, Student, StudentProgress, Branch, Course
from datetime import datetime

faculty_bp = Blueprint('faculty', __name__, url_prefix='/faculty')

@faculty_bp.route('/dashboard')
def dashboard():
    if 'user_id' not in session or session.get('role') != 'faculty':
        return redirect(url_for('auth.login'))

    faculty = Faculty.query.filter_by(user_id=session['user_id']).first()
    if not faculty:
        faculty = Faculty.query.first()

    students = Student.query.filter_by(faculty_id=faculty.faculty_id).all() if faculty else []

    eng_wpms = [s.english_wpm for s in students if s.english_wpm and s.english_wpm > 0]
    avg_eng_wpm = round(sum(eng_wpms) / len(eng_wpms)) if eng_wpms else 0

    kan_wpms = [s.kannada_wpm for s in students if s.kannada_wpm and s.kannada_wpm > 0]
    avg_kan_wpm = round(sum(kan_wpms) / len(kan_wpms)) if kan_wpms else 0

    courses = Course.query.filter_by(status='Active').all()
    active_tab = request.args.get('tab', 'dashboard')

    return render_template(
        'faculty/dashboard.html',
        faculty=faculty,
        students=students,
        courses=courses,
        avg_eng_wpm=avg_eng_wpm,
        avg_kan_wpm=avg_kan_wpm,
        active_tab=active_tab
    )

@faculty_bp.route('/add-student', methods=['POST'])
def add_student():
    if 'user_id' not in session or session.get('role') != 'faculty':
        return redirect(url_for('auth.login'))

    faculty = Faculty.query.filter_by(user_id=session['user_id']).first()
    first_name = request.form.get('first_name', '').strip()
    last_name = request.form.get('last_name', '').strip()
    full_name = f"{first_name} {last_name}".strip()
    reg_no = request.form.get('registration_no', '').strip()
    email = request.form.get('email', '').strip()
    mobile = request.form.get('mobile', '').strip()
    dob_str = request.form.get('dob', '').strip()

    username = f"{first_name.lower()}_{reg_no}"
    password = reg_no

    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        flash(f"Student username '{username}' already exists!", "danger")
        return redirect(url_for("faculty.dashboard", tab="students"))

    new_user = User(
        username=username,
        password_hash=password,
        role='student'
    )
    db.session.add(new_user)
    db.session.flush()

    dob_val = None
    if dob_str:
        try:
            dob_val = datetime.strptime(dob_str, "%Y-%m-%d").date()
        except ValueError:
            pass

    new_student = Student(
        user_id=new_user.user_id,
        branch_id=faculty.branch_id if faculty else 1,
        faculty_id=faculty.faculty_id if faculty else None,
        registration_no=reg_no,
        student_name=full_name,
        mobile=mobile,
        email=email,
        dob=dob_val,
        status='Active'
    )
    db.session.add(new_student)
    db.session.commit()

    flash(f"Student '{full_name}' registered successfully! Username: {username}", "success")
    return redirect(url_for("faculty.dashboard", tab="students"))

@faculty_bp.route('/student/update/<int:student_id>', methods=['POST'])
def update_student(student_id):
    if 'user_id' not in session or session.get('role') != 'faculty':
        return redirect(url_for('auth.login'))

    student = Student.query.get_or_404(student_id)
    first_name = request.form.get("first_name", "").strip()
    last_name = request.form.get("last_name", "").strip()
    student.student_name = f"{first_name} {last_name}".strip()
    student.registration_no = request.form.get("registration_no", "").strip()
    student.mobile = request.form.get("mobile", "").strip()
    student.email = request.form.get("email", "").strip()
    student.status = request.form.get("status", "Active")

    if request.form.get("dob"):
        try:
            student.dob = datetime.strptime(request.form.get("dob"), "%Y-%m-%d").date()
        except ValueError:
            pass

    db.session.commit()
    flash("Student details updated successfully!", "success")
    return redirect(url_for("faculty.dashboard", tab="students"))

@faculty_bp.route('/student/reset/<int:student_id>', methods=['POST'])
def reset_student_password(student_id):
    if 'user_id' not in session or session.get('role') != 'faculty':
        return redirect(url_for('auth.login'))

    student = Student.query.get_or_404(student_id)
    new_password = request.form.get("password", "").strip()
    if student.user_id:
        user = User.query.get(student.user_id)
        if user and new_password:
            user.password_hash = new_password
            db.session.commit()
            flash("Student password updated successfully!", "success")

    return redirect(url_for("faculty.dashboard", tab="students"))

@faculty_bp.route('/student/delete/<int:student_id>', methods=['POST'])
def delete_student(student_id):
    if 'user_id' not in session or session.get('role') != 'faculty':
        return redirect(url_for('auth.login'))

    student = Student.query.get_or_404(student_id)
    if student.user_id:
        user = User.query.get(student.user_id)
        if user:
            db.session.delete(user)

    db.session.delete(student)
    db.session.commit()
    flash("Student deleted successfully!", "success")
    return redirect(url_for("faculty.dashboard", tab="students"))

@faculty_bp.route('/student/<int:student_id>/details')
def student_details(student_id):
    if 'user_id' not in session or session.get('role') != 'faculty':
        return redirect(url_for('auth.login'))

    faculty = Faculty.query.filter_by(user_id=session['user_id']).first()
    if not faculty:
        faculty = Faculty.query.first()

    student = Student.query.get_or_404(student_id)
    branch = Branch.query.get(student.branch_id) if student.branch_id else None
    if not branch:
        branch = Branch.query.first()

    progress_records = StudentProgress.query.filter_by(student_id=student_id).all()
    completed_records = [p for p in progress_records if p.status == 'Completed']

    total_seconds = sum(p.time_taken or 0 for p in completed_records)
    mins = total_seconds // 60
    secs = total_seconds % 60
    overall_time_str = f"{mins} mins {secs} secs" if mins > 0 else (f"{secs} secs" if secs > 0 else "--")

    wpms = [p.wpm for p in completed_records if p.wpm]
    avg_wpm = round(sum(wpms) / len(wpms)) if wpms else (student.english_wpm or 0)

    accuracies = [p.accuracy for p in completed_records if p.accuracy]
    avg_accuracy = round(sum(accuracies) / len(accuracies)) if accuracies else 96

    lessons_count = len(completed_records)
    courses = Course.query.filter_by(status='Active').all()
    completed_lesson_ids = [p.lesson_id for p in completed_records]

    course_stats = {}
    for c in courses:
        active_lessons = [l for l in c.lessons if len(l.screens) > 0]
        total_lessons = len(active_lessons) if active_lessons else len(c.lessons)
        comp_count = sum(1 for l in (active_lessons or c.lessons) if l.lesson_id in completed_lesson_ids)
        pct = round((comp_count / total_lessons) * 100) if total_lessons > 0 else 100
        course_stats[c.course_id] = {
            'total_lessons': len(c.lessons),
            'active_lessons_count': total_lessons,
            'completed_count': comp_count,
            'pct': pct
        }

    active_subtab = request.args.get('subtab') or request.args.get('active_subtab') or 'overview'

    return render_template(
        'faculty/student_details.html',
        faculty=faculty,
        branch=branch,
        student=student,
        completed_records=completed_records,
        completed_lesson_ids=completed_lesson_ids,
        overall_time_str=overall_time_str,
        avg_wpm=avg_wpm,
        avg_accuracy=avg_accuracy,
        lessons_count=lessons_count,
        courses=courses,
        course_stats=course_stats,
        active_subtab=active_subtab
    )
