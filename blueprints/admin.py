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
        user = User(
            role="Faculty",
            username=request.form["username"],
            password_hash=request.form["password"],
            status="Active"
        )
        db.session.add(user)
        db.session.commit()

        fac = Faculty(
            branch_id=request.form["branch_id"],
            faculty_name=request.form["faculty_name"],
            qualification=request.form["qualification"],
            experience=request.form["experience"],
            mobile=request.form["mobile"],
            email=request.form["email"],
            user_id=user.user_id,
            status="Active"
        )
        db.session.add(fac)
        db.session.commit()

        fac.faculty_code = f"GIT{fac.faculty_id:04d}"
        db.session.commit()
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

# --- STUDENT MANAGEMENT ---
@admin_bp.route("/students", methods=["GET", "POST"])
def students():
    if request.method == "POST":
        first_name = request.form["first_name"].strip()
        last_name = request.form["last_name"].strip()
        student_name = first_name + " " + last_name
        username = first_name.lower().replace(" ", "") + "_" + request.form["registration_no"]
        password = request.form["registration_no"]
        courses = ",".join(request.form.getlist("course"))

        # Check if user already exists
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash("A user with this username already exists!", "danger")
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
            registration_no=request.form["registration_no"],
            student_name=student_name,
            gender=request.form.get("gender", "Female"),
            dob=datetime.strptime(request.form["dob"], "%Y-%m-%d").date() if request.form.get("dob") else None,
            mobile=request.form.get("mobile"),
            email=request.form.get("email"),
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
        return redirect(url_for("admin.students"))
    
    all_students = Student.query.all()
    branches = Branch.query.all()
    faculties = Faculty.query.all()
    courses = Course.query.filter_by(status="Active").all() if 'Course' in globals() else []
    return render_template("admin/students.html", students=all_students, branches=branches, faculties=faculties, courses=courses)

@admin_bp.route("/student/update/<int:student_id>", methods=["POST"])
def update_student(student_id):
    student = Student.query.get_or_404(student_id)
    student.registration_no = request.form["registration_no"]
    student.student_name = request.form["first_name"] + " " + request.form["last_name"]
    student.gender = request.form["gender"]
    student.dob = datetime.strptime(request.form["dob"], "%Y-%m-%d").date() if request.form["dob"] else None
    student.mobile = request.form["mobile"]
    student.email = request.form["email"]
    student.branch_id = request.form["branch_id"]
    student.course = ",".join(request.form.getlist("course"))
    student.faculty_id = request.form["faculty_id"]
    student.status = request.form["status"]

    user = User.query.get(student.user_id)
    user.username = request.form["first_name"].lower().replace(" ", "") + "_" + request.form["registration_no"]
    db.session.commit()
    return redirect(url_for("admin.students"))

@admin_bp.route("/student/reset-password/<int:student_id>", methods=["POST"])
def reset_student_password(student_id):
    student = Student.query.get_or_404(student_id)
    user = User.query.get(student.user_id)
    user.password_hash = student.registration_no
    db.session.commit()
    return redirect(url_for("admin.students"))

@admin_bp.route("/student/delete/<int:student_id>", methods=["POST"])
def delete_student(student_id):
    student = Student.query.get_or_404(student_id)
    
    # Also delete the associated user login if it exists
    if student.user_id:
        user = User.query.get(student.user_id)
        if user:
            db.session.delete(user)
            
    db.session.delete(student)
    db.session.commit()
    return redirect(url_for("admin.students"))

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