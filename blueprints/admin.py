from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from database import db
from models import User, Branch, Faculty, Student, Course, Lesson, Screen, StudentProgress, TypingGame
from datetime import datetime

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")

def get_admin_user_id():
    if session.get('admin_user_id'):
        return session['admin_user_id']
    if session.get('role') == 'admin' and session.get('user_id'):
        return session['user_id']
    return None

@admin_bp.before_request
def require_admin_login():
    admin_uid = get_admin_user_id()
    if not admin_uid:
        return redirect(url_for('auth.login', role='admin'))

@admin_bp.route("/dashboard", methods=["GET"])
def dashboard():
    # Query all active students from the database
    all_students = Student.query.all()
    all_branches = Branch.query.all()
    
    # Sort branches by number of students enrolled (most active first)
    sorted_branches = sorted(all_branches, key=lambda b: len(b.students), reverse=True) if all_branches else []
    
    # Pass students and branches to the dashboard template
    return render_template("admin/dashboard.html", students=all_students, branches=sorted_branches)

# --- BRANCH MANAGEMENT ---
@admin_bp.route("/branches", methods=["GET", "POST"])
def branches():
    if request.method == "POST":
        branch_name = request.form.get("branch_name") or request.form.get("name")
        branch_code = request.form.get("code") or request.form.get("branch_code")
        phone = request.form.get("phone")
        email = request.form.get("email")
        status = request.form.get("status", "Active")
        username = request.form.get("username")
        password = request.form.get("password")
        
        user_id = None
        if username and password:
            existing_user = User.query.filter_by(username=username).first()
            if existing_user:
                flash("A user with this username already exists!", "danger")
                return redirect(url_for("admin.branches"))
            
            user = User(
                role="Branch",
                username=username,
                password_hash=password,
                status="Active"
            )
            db.session.add(user)
            db.session.commit()
            user_id = user.user_id

        new_branch = Branch(branch_name=branch_name, branch_code=branch_code, phone=phone, email=email, status=status, user_id=user_id)
        db.session.add(new_branch)
        db.session.commit()
        flash("Branch added successfully with login credentials!", "success")
        return redirect(url_for("admin.branches"))
        
    all_branches = Branch.query.all()
    return render_template("admin/branches.html", branches=all_branches)

@admin_bp.route("/branch/update/<int:branch_id>", methods=["POST"])
def update_branch(branch_id):
    branch = Branch.query.get_or_404(branch_id)
    branch.branch_name = request.form.get("branch_name") or request.form.get("name")
    branch.branch_code = request.form.get("branch_code") or request.form.get("code")
    branch.phone = request.form.get("phone")
    branch.email = request.form.get("email")
    branch.status = request.form.get("status", "Active")

    username = request.form.get("username")
    if username:
        if branch.user:
            branch.user.username = username
        else:
            password = request.form.get("password") or "123456"
            user = User(role="Branch", username=username, password_hash=password, status="Active")
            db.session.add(user)
            db.session.commit()
            branch.user_id = user.user_id

    db.session.commit()
    flash("Branch updated successfully!", "success")
    return redirect(url_for("admin.branches"))

@admin_bp.route("/branch/reset-password/<int:branch_id>", methods=["POST"])
def reset_branch_password(branch_id):
    branch = Branch.query.get_or_404(branch_id)
    if branch.user:
        branch.user.password_hash = request.form["password"]
        db.session.commit()
        flash("Branch password updated successfully!", "success")
    else:
        # Create user if missing
        password = request.form["password"]
        username = branch.branch_code.lower()
        user = User(role="Branch", username=username, password_hash=password, status="Active")
        db.session.add(user)
        db.session.commit()
        branch.user_id = user.user_id
        db.session.commit()
        flash("Branch login user created and password set!", "success")
    return redirect(url_for("admin.branches"))

@admin_bp.route("/branch/delete/<int:branch_id>", methods=["POST"])
def delete_branch(branch_id):
    branch = Branch.query.get_or_404(branch_id)
    
    # Delete related records first to prevent foreign key constraint conflicts
    Faculty.query.filter_by(branch_id=branch_id).delete()
    Student.query.filter_by(branch_id=branch_id).delete()

    if branch.user_id:
        user = User.query.get(branch.user_id)
        if user:
            db.session.delete(user)
    
    db.session.delete(branch)
    db.session.commit()
    flash("Branch deleted successfully!", "success")
    return redirect(url_for("admin.branches"))

@admin_bp.route("/branch/<int:branch_id>/details", methods=["GET"])
def branch_details(branch_id):
    branch = Branch.query.get_or_404(branch_id)
    students = Student.query.filter_by(branch_id=branch_id).all()
    faculties = Faculty.query.all()
    return render_template("admin/branch_details.html", branch=branch, students=students, faculties=faculties)

# --- FACULTY MANAGEMENT ---
@admin_bp.route("/faculty", methods=["GET", "POST"])
def faculty():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()

        if not username or not password:
            flash("Username and Password are required!", "danger")
            return redirect(url_for("admin.faculty"))

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash(f"Username '{username}' is already taken! Please choose a different username.", "danger")
            return redirect(url_for("admin.faculty"))

        try:
            user = User(
                role="Faculty",
                username=username,
                password_hash=password,
                status="Active"
            )
            db.session.add(user)
            db.session.flush()

            fac = Faculty(
                branch_id=request.form.get("branch_id"),
                faculty_name=request.form.get("faculty_name"),
                qualification=request.form.get("qualification"),
                experience=request.form.get("experience"),
                mobile=request.form.get("mobile"),
                email=request.form.get("email"),
                user_id=user.user_id,
                status="Active"
            )
            db.session.add(fac)
            db.session.flush()

            fac.faculty_code = f"GIT{fac.faculty_id:04d}"
            db.session.commit()
            flash(f"Faculty '{fac.faculty_name}' created successfully!", "success")
        except Exception as e:
            db.session.rollback()
            flash(f"Error creating faculty: {str(e)}", "danger")

        return redirect(url_for("admin.faculty"))

    faculties = Faculty.query.all()
    branches = Branch.query.all()
    return render_template("admin/faculty.html", faculties=faculties, branches=branches)

@admin_bp.route("/faculty/update/<int:faculty_id>", methods=["POST"])
def update_faculty(faculty_id):
    fac = Faculty.query.get_or_404(faculty_id)
    fac.faculty_name = request.form["faculty_name"]
    fac.qualification = request.form["qualification"]
    fac.experience = request.form["experience"]
    fac.mobile = request.form["mobile"]
    fac.email = request.form["email"]
    db.session.commit()
    return redirect(url_for("admin.faculty"))

@admin_bp.route("/faculty/reset/<int:faculty_id>", methods=["POST"])
def reset_faculty_password(faculty_id):
    fac = Faculty.query.get_or_404(faculty_id)
    user = User.query.get(fac.user_id)
    user.password_hash = request.form["password"]
    db.session.commit()
    return redirect(url_for("admin.faculty"))

@admin_bp.route("/faculty/<int:faculty_id>/details", methods=["GET"])
def faculty_details(faculty_id):
    faculty = Faculty.query.get_or_404(faculty_id)
    branch = Branch.query.get(faculty.branch_id) if faculty.branch_id else None
    return render_template("admin/faculty_details.html", faculty=faculty, branch=branch)

@admin_bp.route("/faculty/delete/<int:faculty_id>")
def delete_faculty(faculty_id):
    fac = Faculty.query.get_or_404(faculty_id)
    user = User.query.get(fac.user_id)
    if user:
        db.session.delete(user)
    db.session.delete(fac)
    db.session.commit()
    return redirect(url_for("admin.faculty"))

def human_relative_time(dt):
    if not dt:
        return "--"
    now = datetime.now()
    diff = now - dt
    seconds = int(diff.total_seconds())
    if seconds < 0:
        return "just now"
    if seconds < 60:
        return f"{seconds} seconds ago"
    minutes = seconds // 60
    if minutes < 60:
        return "1 minute ago" if minutes == 1 else f"{minutes} minutes ago"
    hours = minutes // 60
    if hours < 24:
        return "an hour ago" if hours == 1 else f"{hours} hours ago"
    days = hours // 24
    if days < 30:
        return "a day ago" if days == 1 else f"{days} days ago"
    months = days // 30
    if months < 12:
        return "a month ago" if months == 1 else f"{months} months ago"
    years = days // 365
    return "a year ago" if years == 1 else f"{years} years ago"

def format_typing_time(total_seconds):
    if not total_seconds or total_seconds <= 0:
        return "0:00"
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60
    if hours > 0:
        return f"{hours}:{minutes:02d}:{seconds:02d}"
    return f"{minutes}:{seconds:02d}"

# --- STUDENT MANAGEMENT ---
@admin_bp.route("/students", methods=["GET", "POST"])
def students():
    if request.method == "POST":
        first_name = request.form.get("first_name", "").strip()
        last_name = request.form.get("last_name", "").strip()
        student_name = f"{first_name} {last_name}".strip()
        reg_no = request.form.get("registration_no", "").strip()
        
        username = (first_name.lower().replace(" ", "") if first_name else "user") + "_" + reg_no
        password = reg_no
        courses = ",".join(request.form.getlist("course"))
        if not courses:
            courses = request.form.get("course_single") or "English & Kannada Typing"

        # Check if user already exists
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash(f"A user with username '{username}' already exists!", "danger")
            return redirect(url_for("admin.students"))

        user = User(
            role="Student",
            username=username,
            password_hash=password,
            status="Active"
        )
        db.session.add(user)
        db.session.commit()

        student = Student(
            registration_no=reg_no,
            student_name=student_name,
            gender=request.form.get("gender", "Female"),
            dob=datetime.strptime(request.form["dob"], "%Y-%m-%d").date() if request.form.get("dob") else None,
            mobile=request.form.get("mobile", ""),
            email=request.form.get("email", ""),
            branch_id=request.form["branch_id"],
            course=courses,
            faculty_id=request.form["faculty_id"],
            english_wpm=0,
            kannada_wpm=0,
            user_id=user.user_id,
            status=request.form.get("status", "Active")
        )
        db.session.add(student)
        db.session.commit()
        flash(f"Student '{student_name}' successfully registered!", "success")
        return redirect(url_for("admin.students"))
    
    all_students = Student.query.all()
    branches = Branch.query.all()
    faculties = Faculty.query.all()
    courses = Course.query.filter_by(status="Active").all() if 'Course' in globals() else []

    # Calculate statistics & metrics for each student
    enriched_students = []
    for s in all_students:
        name_parts = (s.student_name or "").strip().split()
        f_name = name_parts[0] if name_parts else "--"
        l_name = " ".join(name_parts[1:]) if len(name_parts) > 1 else "--"
        u_name = s.user.username if s.user else s.registration_no

        # Progress stats
        progress_records = StudentProgress.query.filter_by(student_id=s.student_id).all()
        total_time_secs = sum(p.time_taken or 0 for p in progress_records)
        
        valid_wpms = [p.wpm for p in progress_records if p.wpm and p.wpm > 0]
        avg_wpm = round(sum(valid_wpms) / len(valid_wpms)) if valid_wpms else (s.english_wpm if (s.english_wpm and s.english_wpm > 0) else None)
        
        valid_accs = [p.accuracy for p in progress_records if p.accuracy and p.accuracy > 0]
        avg_acc = round(sum(valid_accs) / len(valid_accs)) if valid_accs else None
        
        latest_date = None
        if progress_records:
            dates = [p.completed_on for p in progress_records if p.completed_on]
            if dates:
                latest_date = max(dates)

        # Formatting
        typing_time_str = format_typing_time(total_time_secs)
        avg_speed_str = f"{avg_wpm} WPM" if avg_wpm else "--"
        avg_acc_str = f"{avg_acc}%" if avg_acc else "--"
        last_login_str = human_relative_time(latest_date)

        # Determine if new (e.g. no progress yet or recently added)
        is_new = (len(progress_records) == 0)

        enriched_students.append({
            'student_id': s.student_id,
            'registration_no': s.registration_no,
            'student_name': s.student_name,
            'first_name': f_name,
            'last_name': l_name,
            'username': u_name,
            'branch': s.branch.branch_name if s.branch else '--',
            'branch_id': s.branch_id,
            'faculty': s.faculty.faculty_name if s.faculty else '--',
            'faculty_id': s.faculty_id,
            'course': s.course or 'English & Kannada Typing',
            'mobile': s.mobile or '--',
            'email': s.email or '',
            'gender': s.gender or 'Female',
            'dob': s.dob.strftime('%Y-%m-%d') if s.dob else '',
            'status': s.status or 'Active',
            'last_login_human': last_login_str,
            'last_login_raw': latest_date.isoformat() if latest_date else '',
            'typing_time_str': typing_time_str,
            'total_time_secs': total_time_secs,
            'avg_speed_str': avg_speed_str,
            'avg_wpm_num': avg_wpm or 0,
            'avg_acc_str': avg_acc_str,
            'avg_acc_num': avg_acc or 0,
            'is_new': is_new,
            'user': s.user
        })

    return render_template(
        "admin/students.html", 
        students=enriched_students, 
        branches=branches, 
        faculties=faculties, 
        courses=courses
    )

@admin_bp.route("/student/update/<int:student_id>", methods=["POST"])
def update_student(student_id):
    student = Student.query.get_or_404(student_id)
    first_name = request.form.get("first_name", "").strip()
    last_name = request.form.get("last_name", "").strip()
    student.registration_no = request.form.get("registration_no", student.registration_no)
    student.student_name = f"{first_name} {last_name}".strip()
    student.gender = request.form.get("gender", student.gender or "Female")
    student.dob = datetime.strptime(request.form["dob"], "%Y-%m-%d").date() if request.form.get("dob") else None
    student.mobile = request.form.get("mobile", student.mobile)
    student.email = request.form.get("email", student.email)
    student.branch_id = request.form.get("branch_id", student.branch_id)
    courses = ",".join(request.form.getlist("course"))
    if courses:
        student.course = courses
    student.faculty_id = request.form.get("faculty_id", student.faculty_id)
    student.status = request.form.get("status", student.status)

    if student.user:
        if first_name:
            student.user.username = first_name.lower().replace(" ", "") + "_" + student.registration_no
        student.user.status = student.status
    db.session.commit()
    flash(f"Student details updated successfully.", "success")
    return redirect(url_for("admin.students"))

@admin_bp.route("/student/reset-password/<int:student_id>", methods=["POST"])
def reset_student_password(student_id):
    student = Student.query.get_or_404(student_id)
    if student.user:
        student.user.password_hash = student.registration_no
        db.session.commit()
        flash(f"Password reset to '{student.registration_no}' for {student.student_name}.", "success")
    return redirect(url_for("admin.students"))

@admin_bp.route("/student/delete/<int:student_id>", methods=["POST"])
def delete_student(student_id):
    student = Student.query.get_or_404(student_id)
    
    if student.user_id:
        user = User.query.get(student.user_id)
        if user:
            db.session.delete(user)
    StudentProgress.query.filter_by(student_id=student.student_id).delete()
    db.session.delete(student)
    db.session.commit()
    flash("Student deleted successfully.", "success")
    return redirect(url_for("admin.students"))

@admin_bp.route("/students/bulk-delete", methods=["POST"])
def bulk_delete_students():
    raw_ids = request.form.get("selected_ids", "")
    student_ids = [int(x.strip()) for x in raw_ids.split(",") if x.strip().isdigit()]
    count = 0
    for sid in student_ids:
        student = Student.query.get(sid)
        if student:
            if student.user_id:
                user = User.query.get(student.user_id)
                if user:
                    db.session.delete(user)
            StudentProgress.query.filter_by(student_id=student.student_id).delete()
            db.session.delete(student)
            count += 1
    db.session.commit()
    flash(f"Successfully deleted {count} student(s).", "success")
    return redirect(url_for("admin.students"))

@admin_bp.route("/students/bulk-reset-password", methods=["POST"])
def bulk_reset_password():
    raw_ids = request.form.get("selected_ids", "")
    student_ids = [int(x.strip()) for x in raw_ids.split(",") if x.strip().isdigit()]
    count = 0
    for sid in student_ids:
        student = Student.query.get(sid)
        if student and student.user:
            student.user.password_hash = student.registration_no
            count += 1
    db.session.commit()
    flash(f"Successfully reset password for {count} student(s) to their registration number.", "success")
    return redirect(url_for("admin.students"))

@admin_bp.route("/students/seed-demo", methods=["POST", "GET"])
def seed_demo_students():
    # Seed the authentic sample student records from the screenshot
    demo_data = [
        {"reg": "1516705", "first": "", "last": "", "username": "git_123", "secs": 0, "wpm": 0, "acc": 0, "days_ago": 11},
        {"reg": "1516700", "first": "", "last": "", "username": "indra_1516700", "secs": 2216, "wpm": 13, "acc": 92, "days_ago": 0.8},
        {"reg": "1516706", "first": "", "last": "", "username": "mallika_1516706", "secs": 2406, "wpm": 12, "acc": 96, "days_ago": 0.8},
        {"reg": "1516701", "first": "", "last": "", "username": "swapna_1516701", "secs": 1979, "wpm": 17, "acc": 95, "days_ago": 0.8},
        {"reg": "1516709", "first": "", "last": "", "username": "inchara_1516709", "secs": 1367, "wpm": 17, "acc": 90, "days_ago": 0.01},
        {"reg": "1516644", "first": "", "last": "", "username": "prabhath_1516644", "secs": 0, "wpm": 0, "acc": 0, "days_ago": 6},
        {"reg": "1516720", "first": "", "last": "", "username": "latha_1516720", "secs": 911, "wpm": 25, "acc": 95, "days_ago": 0.85},
        {"reg": "1516623", "first": "", "last": "", "username": "sushil_1516623", "secs": 0, "wpm": 0, "acc": 0, "days_ago": 4},
        {"reg": "1516692", "first": "", "last": "", "username": "muzammil_1516692", "secs": 1463, "wpm": 11, "acc": 81, "days_ago": 0.75},
        {"reg": "1516676", "first": "", "last": "", "username": "1516676", "secs": 2280, "wpm": 12, "acc": 95, "days_ago": 0.05},
        {"reg": "1516675", "first": "", "last": "", "username": "jashwanth_1516675", "secs": 674, "wpm": 14, "acc": 95, "days_ago": 0.05},
        {"reg": "1516667", "first": "", "last": "", "username": "mamatha_1516667", "secs": 1627, "wpm": 24, "acc": 95, "days_ago": 1.1},
        {"reg": "1516881", "first": "", "last": "", "username": "pavithra_1516881", "secs": 6302, "wpm": 14, "acc": 96, "days_ago": 0.1},
        {"reg": "1516686", "first": "", "last": "", "username": "rakshitha_1516686", "secs": 837, "wpm": 17, "acc": 93, "days_ago": 1.2},
        {"reg": "1516708", "first": "", "last": "", "username": "sashikala_1516708", "secs": 0, "wpm": 0, "acc": 0, "days_ago": 12},
        {"reg": "1516573", "first": "", "last": "", "username": "teju_1516573", "secs": 1582, "wpm": 24, "acc": 92, "days_ago": 0.1},
        {"reg": "1516598", "first": "", "last": "", "username": "ashwini_1516598", "secs": 0, "wpm": 0, "acc": 0, "days_ago": 10},
        {"reg": "1516725", "first": "AMRUTHAVANI", "last": "M", "username": "amruthavani", "secs": 0, "wpm": 0, "acc": 0, "days_ago": None},
        {"reg": "1516670", "first": "Hemanth", "last": "M", "username": "hemanth_1516670", "secs": 3554, "wpm": 15, "acc": 97, "days_ago": 4},
        {"reg": "1516636", "first": "Manusree", "last": "K S", "username": "manu_1516636", "secs": 0, "wpm": 0, "acc": 0, "days_ago": 2},
        {"reg": "1516723", "first": "Manyashree", "last": "M", "username": "manya_1516723", "secs": 69, "wpm": 16, "acc": 99, "days_ago": 0.85},
    ]

    branch = Branch.query.first()
    faculty = Faculty.query.first()
    b_id = branch.branch_id if branch else 1
    f_id = faculty.faculty_id if faculty else 1

    from datetime import timedelta
    now = datetime.now()

    for item in demo_data:
        existing = Student.query.filter_by(registration_no=item["reg"]).first()
        if not existing:
            user = User.query.filter_by(username=item["username"]).first()
            if not user:
                user = User(
                    role="Student",
                    username=item["username"],
                    password_hash=item["reg"],
                    status="Active"
                )
                db.session.add(user)
                db.session.commit()

            s_name = f"{item['first']} {item['last']}".strip()
            student = Student(
                registration_no=item["reg"],
                student_name=s_name if s_name else item["username"],
                gender="Female",
                branch_id=b_id,
                faculty_id=f_id,
                course="English & Kannada Typing",
                mobile="9876543210",
                english_wpm=item["wpm"],
                user_id=user.user_id,
                status="Active"
            )
            db.session.add(student)
            db.session.commit()

            if item["secs"] > 0 or item["wpm"] > 0:
                completed_time = now - timedelta(days=item["days_ago"]) if item["days_ago"] is not None else None
                progress = StudentProgress(
                    student_id=student.student_id,
                    lesson_id=1,
                    wpm=item["wpm"],
                    accuracy=float(item["acc"]),
                    mistakes=2,
                    time_taken=item["secs"],
                    completed_on=completed_time,
                    status="Completed"
                )
                db.session.add(progress)
                db.session.commit()

    flash("Sample student records loaded successfully!", "success")
    return redirect(url_for("admin.students"))

@admin_bp.route('/student/<int:student_id>/details')
def student_details(student_id):
    student = Student.query.get_or_404(student_id)
    branch = student.branch or Branch.query.first()
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
    courses = Course.query.filter_by(status='Active').all() if 'Course' in globals() else []
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
        is_faculty=False,
        is_admin=True
    )

# --- LMS CONTENT MANAGEMENT ---
@admin_bp.route("/lms-content", methods=["GET", "POST"])
def lms_content():
    if request.method == "POST":
        if "game_name" in request.form:
            game = TypingGame(
                game_name=request.form["game_name"],
                category=request.form.get("category", "Speed & Accuracy"),
                difficulty=request.form.get("difficulty", "Medium"),
                status=request.form.get("status", "Active")
            )
            db.session.add(game)
            db.session.commit()
            return redirect(url_for("admin.lms_content"))
        else:
            course = Course(
                course_name=request.form["course_name"],
                status=request.form["status"]
            )
            db.session.add(course)
            db.session.commit()
            return redirect(url_for("admin.lms_content"))

    courses = Course.query.all()
    games = TypingGame.query.all()
    return render_template("admin/lms_content.html", courses=courses, games=games)

@admin_bp.route("/course/update/<int:course_id>", methods=["POST"])
def update_course(course_id):
    course = Course.query.get_or_404(course_id)
    course.course_name = request.form["course_name"]
    course.status = request.form["status"]
    db.session.commit()
    return redirect(url_for("admin.lms_content"))

@admin_bp.route("/course/delete/<int:course_id>")
def delete_course(course_id):
    course = Course.query.get_or_404(course_id)
    # Explicitly clean up all child lessons, screens, and progress records
    lessons = Lesson.query.filter_by(course_id=course_id).all()
    for l in lessons:
        Screen.query.filter_by(lesson_id=l.lesson_id).delete()
        StudentProgress.query.filter_by(lesson_id=l.lesson_id).delete()
        db.session.delete(l)
    db.session.delete(course)
    db.session.commit()
    return redirect(url_for("admin.lms_content"))

@admin_bp.route("/game/update/<int:game_id>", methods=["POST"])
def update_game(game_id):
    game = TypingGame.query.get_or_404(game_id)
    game.game_name = request.form["game_name"]
    game.category = request.form.get("category", game.category)
    game.difficulty = request.form.get("difficulty", game.difficulty)
    game.status = request.form["status"]
    db.session.commit()
    return redirect(url_for("admin.lms_content"))

@admin_bp.route("/game/delete/<int:game_id>")
def delete_game(game_id):
    game = TypingGame.query.get_or_404(game_id)
    db.session.delete(game)
    db.session.commit()
    return redirect(url_for("admin.lms_content"))

@admin_bp.route("/course/<int:course_id>/lessons")
def manage_lessons(course_id):
    course = Course.query.get_or_404(course_id)
    active_chapter = request.args.get("chapter", "all")
    chapter_order = {'Beginner': 1, 'Intermediate': 2, 'Advanced': 3}
    lessons = Lesson.query.filter_by(course_id=course_id).all()
    lessons = sorted(lessons, key=lambda l: (chapter_order.get(l.chapter or 'Beginner', 1), l.display_order or 0, l.lesson_id))
    return render_template("admin/lesson.html", course=course, lessons=lessons, active_chapter=active_chapter)

@admin_bp.route("/course/<int:course_id>/lesson/add", methods=["POST"])
def add_lesson(course_id):
    chapter = request.form.get("chapter", "Beginner")
    display_order = Lesson.query.filter_by(course_id=course_id, chapter=chapter).count() + 1
    lesson = Lesson(
        course_id=course_id,
        lesson_title=request.form["lesson_title"],
        lesson_description=request.form["lesson_description"],
        chapter=chapter,
        display_order=display_order,
        status=request.form["status"]
    )
    db.session.add(lesson)
    db.session.commit()
    return redirect(url_for("admin.manage_lessons", course_id=course_id, chapter=chapter))

@admin_bp.route("/lesson/update/<int:lesson_id>", methods=["POST"])
def update_lesson(lesson_id):
    lesson = Lesson.query.get_or_404(lesson_id)
    old_chapter = lesson.chapter or "Beginner"
    new_chapter = request.form.get("chapter", old_chapter)
    lesson.lesson_title = request.form["lesson_title"]
    lesson.lesson_description = request.form["lesson_description"]
    
    if old_chapter != new_chapter:
        lesson.chapter = new_chapter
        lesson.display_order = Lesson.query.filter_by(course_id=lesson.course_id, chapter=new_chapter).count() + 1
    
    lesson.status = request.form["status"]
    db.session.commit()
    
    # Re-sequence old chapter lessons if chapter changed
    if old_chapter != new_chapter:
        old_remaining = Lesson.query.filter_by(course_id=lesson.course_id, chapter=old_chapter).order_by(Lesson.display_order, Lesson.lesson_id).all()
        for idx, l in enumerate(old_remaining, 1):
            l.display_order = idx
        db.session.commit()

    return redirect(url_for("admin.manage_lessons", course_id=lesson.course_id, chapter=new_chapter))

@admin_bp.route("/lesson/delete/<int:lesson_id>")
def delete_lesson(lesson_id):
    lesson = Lesson.query.get_or_404(lesson_id)
    course_id = lesson.course_id
    chapter = lesson.chapter or "Beginner"
    
    # Explicitly clean up child screens & progress records
    Screen.query.filter_by(lesson_id=lesson_id).delete()
    StudentProgress.query.filter_by(lesson_id=lesson_id).delete()
    
    db.session.delete(lesson)
    db.session.commit()
    
    # Re-sequence remaining lessons in this chapter to ensure no gaps
    remaining = Lesson.query.filter_by(course_id=course_id, chapter=chapter).order_by(Lesson.display_order, Lesson.lesson_id).all()
    for idx, l in enumerate(remaining, 1):
        l.display_order = idx
    db.session.commit()
    
    return redirect(url_for("admin.manage_lessons", course_id=course_id, chapter=chapter))

@admin_bp.route("/lesson/<int:lesson_id>/screens")
def manage_screens(lesson_id):
    lesson = Lesson.query.get_or_404(lesson_id)
    screens = Screen.query.filter_by(lesson_id=lesson_id).order_by(Screen.display_order).all()
    return render_template("admin/screens.html", lesson=lesson, screens=screens)

@admin_bp.route("/lesson/<int:lesson_id>/screen/add", methods=["POST"])
def add_screen(lesson_id):
    display_order = Screen.query.filter_by(lesson_id=lesson_id).count() + 1
    screen_type = request.form.get("screen_type", "block")
    screen = Screen(
        lesson_id=lesson_id,
        screen_title=request.form["screen_title"],
        screen_content=request.form["screen_content"],
        screen_type=screen_type,
        display_order=display_order,
        status=request.form["status"]
    )
    db.session.add(screen)
    db.session.commit()
    return redirect(url_for("admin.manage_screens", lesson_id=lesson_id))

@admin_bp.route("/lesson/screen/update/<int:screen_id>", methods=["POST"])
def update_screen(screen_id):
    screen = Screen.query.get_or_404(screen_id)
    screen.screen_title = request.form["screen_title"]
    screen.screen_content = request.form["screen_content"]
    screen.screen_type = request.form.get("screen_type", screen.screen_type or "block")
    screen.status = request.form["status"]
    db.session.commit()
    return redirect(url_for("admin.manage_screens", lesson_id=screen.lesson_id))

@admin_bp.route("/screen/delete/<int:screen_id>")
def delete_screen(screen_id):
    screen = Screen.query.get_or_404(screen_id)
    lesson_id = screen.lesson_id
    db.session.delete(screen)
    db.session.commit()
    return redirect(url_for("admin.manage_screens", lesson_id=lesson_id))