from flask import Blueprint, render_template, session, redirect, url_for, request, flash
from database import db
from models import User, Branch, Faculty, Student, StudentProgress, Course, Lesson
from datetime import datetime, timedelta
import json

branch_bp = Blueprint('branch', __name__, url_prefix='/branch')

def get_branch_user_id():
    if session.get('branch_user_id'):
        return session['branch_user_id']
    if session.get('role') in ['branch', 'branch_admin', 'branch admin'] and session.get('user_id'):
        return session['user_id']
    return None

@branch_bp.route('/dashboard')
def dashboard():
    branch_user_id = get_branch_user_id()
    if not branch_user_id:
        return redirect(url_for('auth.login', role='branch'))
    
    branch = Branch.query.filter_by(user_id=branch_user_id).first()
    if not branch:
        branch = Branch.query.first()

    faculties = Faculty.query.filter_by(branch_id=branch.branch_id).all() if branch else []
    students = Student.query.filter_by(branch_id=branch.branch_id).all() if branch else []
    courses = Course.query.filter_by(status='Active').all()

    # Calculate Teacher Activity metrics dynamically from DB
    teacher_activity = []
    for f in faculties:
        fac_students = Student.query.filter_by(faculty_id=f.faculty_id).all()
        student_ids = [s.student_id for s in fac_students]
        
        progress_records = StudentProgress.query.filter(
            StudentProgress.student_id.in_(student_ids),
            StudentProgress.status == 'Completed'
        ).all() if student_ids else []

        total_seconds = sum(p.time_taken or 0 for p in progress_records)
        hours = total_seconds // 3600
        mins = (total_seconds % 3600) // 60
        time_str = f"{hours} hrs {mins} mins" if hours > 0 else f"{mins} mins"

        wpms = [p.wpm for p in progress_records if p.wpm]
        avg_wpm = round(sum(wpms) / len(wpms)) if wpms else (round(sum(s.english_wpm for s in fac_students if s.english_wpm) / len(fac_students)) if fac_students else 18)

        accuracies = [p.accuracy for p in progress_records if p.accuracy]
        avg_acc = round(sum(accuracies) / len(accuracies)) if accuracies else 96

        teacher_activity.append({
            'faculty_id': f.faculty_id,
            'faculty_name': f.faculty_name,
            'faculty_code': f.faculty_code or f"FAC00{f.faculty_id}",
            'time_spent': time_str or "0 mins",
            'total_students': len(fac_students),
            'active_students': len(fac_students),
            'avg_speed': avg_wpm or 18,
            'avg_accuracy': avg_acc or 96
        })

    teacher_activity = sorted(teacher_activity, key=lambda x: x['active_students'], reverse=True)

    # Calculate real daily chart data dynamically from DB StudentProgress records
    branch_student_ids = [s.student_id for s in students]
    today = datetime.now().date()

    dates = []
    this_week_data = []
    last_week_data = []

    for i in range(6, -1, -1):
        target_date = today - timedelta(days=i)
        dates.append(target_date.strftime("%b %d"))

        day_start = datetime.combine(target_date, datetime.min.time())
        day_end = datetime.combine(target_date, datetime.max.time())

        records = StudentProgress.query.filter(
            StudentProgress.student_id.in_(branch_student_ids),
            StudentProgress.status == 'Completed',
            StudentProgress.completed_on >= day_start,
            StudentProgress.completed_on <= day_end
        ).all() if branch_student_ids else []

        total_secs = sum(r.time_taken or 0 for r in records)
        avg_mins = round((total_secs / 60.0) / len(branch_student_ids), 1) if branch_student_ids else 0.0
        this_week_data.append(avg_mins)

        # Query last week same day
        lw_target = target_date - timedelta(days=7)
        lw_start = datetime.combine(lw_target, datetime.min.time())
        lw_end = datetime.combine(lw_target, datetime.max.time())

        lw_records = StudentProgress.query.filter(
            StudentProgress.student_id.in_(branch_student_ids),
            StudentProgress.status == 'Completed',
            StudentProgress.completed_on >= lw_start,
            StudentProgress.completed_on <= lw_end
        ).all() if branch_student_ids else []

        lw_total_secs = sum(r.time_taken or 0 for r in lw_records)
        lw_avg_mins = round((lw_total_secs / 60.0) / len(branch_student_ids), 1) if branch_student_ids else 0.0
        last_week_data.append(lw_avg_mins)

    eng_wpms = [s.english_wpm for s in students if s.english_wpm and s.english_wpm > 0]
    avg_eng_wpm = round(sum(eng_wpms) / len(eng_wpms)) if eng_wpms else 0

    kan_wpms = [s.kannada_wpm for s in students if s.kannada_wpm and s.kannada_wpm > 0]
    avg_kan_wpm = round(sum(kan_wpms) / len(kan_wpms)) if kan_wpms else 0

    active_tab = request.args.get('tab', 'dashboard')

    return render_template(
        'branch/dashboard.html',
        branch=branch,
        faculties=faculties,
        students=students,
        courses=courses,
        avg_eng_wpm=avg_eng_wpm,
        avg_kan_wpm=avg_kan_wpm,
        active_tab=active_tab,
        teacher_activity=teacher_activity,
        chart_labels=json.dumps(dates),
        this_week_data=json.dumps(this_week_data),
        last_week_data=json.dumps(last_week_data)
    )

@branch_bp.route('/student/add', methods=['POST'])
def add_student():
    branch_user_id = get_branch_user_id()
    if not branch_user_id:
        return redirect(url_for('auth.login', role='branch'))

    branch = Branch.query.filter_by(user_id=branch_user_id).first()
    if not branch:
        branch = Branch.query.first()

    first_name = request.form.get("first_name", "").strip()
    last_name = request.form.get("last_name", "").strip()
    registration_no = request.form.get("registration_no", "").strip()
    student_name = f"{first_name} {last_name}".strip()
    username = f"{first_name.lower().replace(' ', '')}_{registration_no}"
    password = registration_no
    courses = ",".join(request.form.getlist("course")) or "English & Kannada Typing"

    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        flash("A student with this registration number/username already exists!", "danger")
        return redirect(url_for("branch.dashboard", tab="students"))

    user = User(
        role="Student",
        username=username,
        password_hash=password,
        status="Active"
    )
    db.session.add(user)
    db.session.commit()

    faculty_id = request.form.get("faculty_id")
    dob_str = request.form.get("dob")
    dob_date = datetime.strptime(dob_str, "%Y-%m-%d").date() if dob_str else None

    student = Student(
        registration_no=registration_no,
        student_name=student_name,
        gender=request.form.get("gender", "Female"),
        dob=dob_date,
        mobile=request.form.get("mobile"),
        email=request.form.get("email"),
        branch_id=branch.branch_id if branch else 1,
        faculty_id=faculty_id if faculty_id else None,
        course=courses,
        english_wpm=0,
        kannada_wpm=0,
        user_id=user.user_id,
        status="Active"
    )
    db.session.add(student)
    db.session.commit()

    flash(f"Student '{student_name}' registered successfully!", "success")
    return redirect(url_for("branch.dashboard", tab="students"))

@branch_bp.route('/student/update/<int:student_id>', methods=['POST'])
def update_student(student_id):
    branch_user_id = get_branch_user_id()
    if not branch_user_id:
        return redirect(url_for('auth.login', role='branch'))

    student = Student.query.get_or_404(student_id)
    first_name = request.form.get("first_name", "").strip()
    last_name = request.form.get("last_name", "").strip()
    student.student_name = f"{first_name} {last_name}".strip()
    student.registration_no = request.form.get("registration_no", "").strip()
    student.mobile = request.form.get("mobile", "").strip()
    student.email = request.form.get("email", "").strip()
    student.faculty_id = request.form.get("faculty_id") or None
    student.status = request.form.get("status", "Active")

    if request.form.get("dob"):
        try:
            student.dob = datetime.strptime(request.form.get("dob"), "%Y-%m-%d").date()
        except ValueError:
            pass

    db.session.commit()
    flash("Student details updated successfully!", "success")
    return redirect(url_for("branch.dashboard", tab="students"))

@branch_bp.route('/student/reset/<int:student_id>', methods=['POST'])
def reset_student_password(student_id):
    branch_user_id = get_branch_user_id()
    if not branch_user_id:
        return redirect(url_for('auth.login', role='branch'))

    student = Student.query.get_or_404(student_id)
    new_password = request.form.get("password", "").strip()
    if student.user_id:
        user = User.query.get(student.user_id)
        if user and new_password:
            user.password_hash = new_password
            db.session.commit()
            flash("Student password updated successfully!", "success")

    return redirect(url_for("branch.dashboard", tab="students"))

@branch_bp.route('/student/delete/<int:student_id>', methods=['POST'])
def delete_student(student_id):
    branch_user_id = get_branch_user_id()
    if not branch_user_id:
        return redirect(url_for('auth.login', role='branch'))

    student = Student.query.get_or_404(student_id)
    if student.user_id:
        user = User.query.get(student.user_id)
        if user:
            db.session.delete(user)
    
    db.session.delete(student)
    db.session.commit()
    flash("Student deleted successfully!", "success")
    return redirect(url_for("branch.dashboard", tab="students"))

@branch_bp.route('/student/<int:student_id>/details')
def student_details(student_id):
    branch_user_id = get_branch_user_id()
    faculty_user_id = session.get('faculty_user_id') or (session.get('user_id') if session.get('role') == 'faculty' else None)
    
    if not branch_user_id and not faculty_user_id:
        return redirect(url_for('auth.login', role='branch'))

    if branch_user_id:
        branch = Branch.query.filter_by(user_id=branch_user_id).first()
    else:
        faculty = Faculty.query.filter_by(user_id=faculty_user_id).first()
        branch = Branch.query.get(faculty.branch_id) if faculty else None
    if not branch:
        branch = Branch.query.first()

    student = Student.query.get_or_404(student_id)
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

    user_role = session.get('role', '').lower()
    is_faculty = (user_role in ['faculty', 'trainer', 'teacher'])
    active_subtab = request.args.get('subtab') or request.args.get('active_subtab') or 'overview'

    return render_template(
        'branch/student_details.html',
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
        active_subtab=active_subtab,
        is_faculty=is_faculty
    )
