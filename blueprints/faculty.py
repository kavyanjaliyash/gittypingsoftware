from flask import Blueprint, render_template, session, redirect, url_for, request, flash
from database import db
from models import User, Faculty, Student, StudentProgress, Branch, Course
from datetime import datetime, timedelta

faculty_bp = Blueprint('faculty', __name__, url_prefix='/faculty')

def get_faculty_user_id():
    if session.get('faculty_user_id'):
        return session['faculty_user_id']
    if session.get('role') == 'faculty' and session.get('user_id'):
        return session['user_id']
    return None

def human_relative_time(dt):
    if not dt:
        return "--"
    now = datetime.now()
    diff = now - dt
    seconds = int(diff.total_seconds())
    if seconds < 0:
        return "just now"
    if seconds < 60:
        return f"{seconds}s ago"
    minutes = seconds // 60
    if minutes < 60:
        return f"{minutes} min ago" if minutes == 1 else f"{minutes} mins ago"
    hours = minutes // 60
    if hours < 24:
        return f"{hours} hour ago" if hours == 1 else f"{hours} hours ago"
    days = hours // 24
    if days < 30:
        return f"{days} day ago" if days == 1 else f"{days} days ago"
    months = days // 30
    if months < 12:
        return f"{months} mo ago" if months == 1 else f"{months} mos ago"
    years = days // 365
    return f"{years} yr ago" if years == 1 else f"{years} yrs ago"

def format_typing_time(seconds):
    if not seconds or seconds <= 0:
        return "0:00"
    m = seconds // 60
    s = seconds % 60
    h = m // 60
    m = m % 60
    if h > 0:
        return f"{h}:{m:02d}:{s:02d}"
    return f"{m}:{s:02d}"

@faculty_bp.route('/students')
def students_redirect():
    return redirect(url_for('faculty.dashboard', tab='students'))

@faculty_bp.route('/dashboard')
def dashboard():
    faculty_user_id = get_faculty_user_id()
    if not faculty_user_id:
        return redirect(url_for('auth.login', role='faculty'))

    faculty = Faculty.query.filter_by(user_id=faculty_user_id).first()
    if not faculty:
        faculty = Faculty.query.first()

    raw_students = Student.query.filter_by(faculty_id=faculty.faculty_id).all() if faculty else []

    # Enrich students with typing metrics
    now = datetime.now()
    seven_days_ago = now - timedelta(days=7)
    students = []
    for student in raw_students:
        progress_records = StudentProgress.query.filter_by(student_id=student.student_id).all()
        completed_records = [p for p in progress_records if p.status == 'Completed']

        total_seconds = sum(p.time_taken or 0 for p in completed_records)
        wpms = [p.wpm for p in completed_records if p.wpm and p.wpm > 0]
        accuracies = [p.accuracy for p in completed_records if p.accuracy is not None]

        avg_wpm = round(sum(wpms) / len(wpms)) if wpms else (student.english_wpm or 0)
        avg_acc = round(sum(accuracies) / len(accuracies)) if accuracies else (96 if wpms else 0)

        latest_progress = max([p.completed_on for p in completed_records if p.completed_on], default=None)
        last_login_raw = latest_progress.isoformat() if latest_progress else ""
        last_login_human = human_relative_time(latest_progress) if latest_progress else "--"

        parts = (student.student_name or "").strip().split(maxsplit=1)
        f_name = parts[0] if len(parts) > 0 else (student.user.username if student.user else "--")
        l_name = parts[1] if len(parts) > 1 else "--"

        is_new = (len(progress_records) == 0)

        students.append({
            "student_id": student.student_id,
            "registration_no": student.registration_no,
            "student_name": student.student_name or f"{f_name} {l_name}".strip(),
            "first_name": f_name,
            "last_name": l_name,
            "username": student.user.username if student.user else f"user_{student.registration_no}",
            "mobile": student.mobile or "--",
            "email": student.email or "--",
            "branch_id": student.branch_id,
            "faculty_id": student.faculty_id,
            "branch": student.branch.branch_name if student.branch else "Main Branch",
            "faculty": student.faculty.faculty_name if student.faculty else (faculty.faculty_name if faculty else "Instructor"),
            "course": student.course or "English & Kannada Typing",
            "last_login_human": last_login_human,
            "last_login_raw": last_login_raw,
            "typing_time_str": format_typing_time(total_seconds),
            "total_time_secs": total_seconds,
            "avg_speed_str": f"{avg_wpm} WPM" if avg_wpm > 0 else "--",
            "avg_wpm_num": avg_wpm,
            "avg_acc_str": f"{avg_acc}%" if avg_acc > 0 else "--",
            "avg_acc_num": avg_acc,
            "is_new": is_new,
            "status": student.status or "Active"
        })

    eng_wpms = [s["avg_wpm_num"] for s in students if s["avg_wpm_num"] > 0]
    avg_eng_wpm = round(sum(eng_wpms) / len(eng_wpms)) if eng_wpms else 0
    avg_kan_wpm = 0

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
    faculty_user_id = get_faculty_user_id()
    if not faculty_user_id:
        return redirect(url_for('auth.login', role='faculty'))

    faculty = Faculty.query.filter_by(user_id=faculty_user_id).first()
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
    faculty_user_id = get_faculty_user_id()
    if not faculty_user_id:
        return redirect(url_for('auth.login', role='faculty'))

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
    faculty_user_id = get_faculty_user_id()
    if not faculty_user_id:
        return redirect(url_for('auth.login', role='faculty'))

    student = Student.query.get_or_404(student_id)
    new_password = request.form.get("password", "").strip()
    if student.user_id:
        user = User.query.get(student.user_id)
        if user and new_password:
            user.password_hash = new_password
            db.session.commit()
            flash("Student password updated successfully!", "success")

    return redirect(url_for("faculty.dashboard", tab="students"))

@faculty_bp.route('/students/bulk-delete', methods=['POST'])
def bulk_delete_students():
    faculty_user_id = get_faculty_user_id()
    if not faculty_user_id:
        return redirect(url_for('auth.login', role='faculty'))

    selected_ids_str = request.form.get("selected_ids", "")
    if selected_ids_str:
        s_ids = [int(x.strip()) for x in selected_ids_str.split(",") if x.strip().isdigit()]
        deleted_count = 0
        for s_id in s_ids:
            student = Student.query.get(s_id)
            if student:
                StudentProgress.query.filter_by(student_id=student.student_id).delete()
                if student.user_id:
                    User.query.filter_by(user_id=student.user_id).delete()
                db.session.delete(student)
                deleted_count += 1
        db.session.commit()
        flash(f"{deleted_count} student(s) deleted successfully.", "success")
    return redirect(url_for("faculty.dashboard", tab="students"))

@faculty_bp.route('/students/bulk-reset-password', methods=['POST'])
def bulk_reset_password():
    faculty_user_id = get_faculty_user_id()
    if not faculty_user_id:
        return redirect(url_for('auth.login', role='faculty'))

    selected_ids_str = request.form.get("selected_ids", "")
    if selected_ids_str:
        s_ids = [int(x.strip()) for x in selected_ids_str.split(",") if x.strip().isdigit()]
        reset_count = 0
        for s_id in s_ids:
            student = Student.query.get(s_id)
            if student and student.user_id:
                user = User.query.get(student.user_id)
                if user:
                    user.password_hash = student.registration_no
                    reset_count += 1
        db.session.commit()
        flash(f"Passwords for {reset_count} student(s) reset to their registration numbers.", "success")
    return redirect(url_for("faculty.dashboard", tab="students"))

@faculty_bp.route('/student/delete/<int:student_id>', methods=['POST'])
def delete_student(student_id):
    faculty_user_id = get_faculty_user_id()
    if not faculty_user_id:
        return redirect(url_for('auth.login', role='faculty'))

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
    faculty_user_id = get_faculty_user_id()
    if not faculty_user_id:
        return redirect(url_for('auth.login', role='faculty'))

    faculty = Faculty.query.filter_by(user_id=faculty_user_id).first()
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
