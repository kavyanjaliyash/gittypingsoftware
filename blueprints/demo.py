from flask import Blueprint, render_template, session, redirect, url_for, request, jsonify
from database import db
from models import Course, Lesson, Screen, Student, User

demo_bp = Blueprint('demo', __name__, url_prefix='/lms')

@demo_bp.route('/demo')
def practice_demo():
    # Check if ANY role is authenticated
    admin_uid = session.get('admin_user_id') or (session.get('user_id') if session.get('role') == 'admin' else None)
    branch_uid = session.get('branch_user_id') or (session.get('user_id') if session.get('role') in ['branch', 'branch_admin', 'branch admin'] else None)
    faculty_uid = session.get('faculty_user_id') or (session.get('user_id') if session.get('role') == 'faculty' else None)
    student_uid = session.get('student_user_id') or (session.get('user_id') if session.get('role') == 'student' else None)

    if not (admin_uid or branch_uid or faculty_uid or student_uid or session.get('user_id')):
        return redirect(url_for('auth.login'))

    portal_arg = request.args.get('portal', '').strip().lower()

    # Priority 1: Explicit portal query parameter
    if portal_arg == 'admin':
        user_role = 'admin'
        portal_name = 'Admin LMS'
        back_url = url_for('admin.lms_content')
    elif portal_arg == 'branch':
        user_role = 'branch'
        portal_name = 'Branch LMS'
        back_url = url_for('branch.dashboard', tab='lms')
    elif portal_arg == 'faculty':
        user_role = 'faculty'
        portal_name = 'Faculty LMS'
        back_url = url_for('faculty.dashboard', tab='lms')
    elif portal_arg == 'student':
        user_role = 'student'
        portal_name = 'Student Dashboard'
        back_url = url_for('student.dashboard')
    else:
        # Priority 2: Check referrer header
        ref = request.referrer or ''
        if '/admin' in ref and admin_uid:
            user_role = 'admin'
            portal_name = 'Admin LMS'
            back_url = url_for('admin.lms_content')
        elif '/branch' in ref and branch_uid:
            user_role = 'branch'
            portal_name = 'Branch LMS'
            back_url = url_for('branch.dashboard', tab='lms')
        elif '/faculty' in ref and faculty_uid:
            user_role = 'faculty'
            portal_name = 'Faculty LMS'
            back_url = url_for('faculty.dashboard', tab='lms')
        elif '/student' in ref and student_uid:
            user_role = 'student'
            portal_name = 'Student Dashboard'
            back_url = url_for('student.dashboard')
        # Priority 3: Check active role from session in priority order
        elif admin_uid:
            user_role = 'admin'
            portal_name = 'Admin LMS'
            back_url = url_for('admin.lms_content')
        elif branch_uid:
            user_role = 'branch'
            portal_name = 'Branch LMS'
            back_url = url_for('branch.dashboard', tab='lms')
        elif faculty_uid:
            user_role = 'faculty'
            portal_name = 'Faculty LMS'
            back_url = url_for('faculty.dashboard', tab='lms')
        elif student_uid:
            user_role = 'student'
            portal_name = 'Student Dashboard'
            back_url = url_for('student.dashboard')
        else:
            role_val = session.get('role', 'student').lower()
            if role_val == 'admin':
                user_role = 'admin'
                portal_name = 'Admin LMS'
                back_url = url_for('admin.lms_content')
            elif role_val in ['branch', 'branch_admin', 'branch admin']:
                user_role = 'branch'
                portal_name = 'Branch LMS'
                back_url = url_for('branch.dashboard', tab='lms')
            elif role_val == 'faculty':
                user_role = 'faculty'
                portal_name = 'Faculty LMS'
                back_url = url_for('faculty.dashboard', tab='lms')
            else:
                user_role = 'student'
                portal_name = 'Student Dashboard'
                back_url = url_for('student.dashboard')

    courses = Course.query.filter_by(status='Active').all()
    if not courses:
        courses = Course.query.all()

    # Requested course, lesson, screen parameters
    course_id = request.args.get('course_id', type=int)
    lesson_id = request.args.get('lesson_id', type=int)
    screen_idx = request.args.get('screen_idx', 0, type=int)

    # Determine current active course
    current_course = None
    if lesson_id:
        lesson_obj = Lesson.query.get(lesson_id)
        if lesson_obj:
            current_course = lesson_obj.course
            course_id = lesson_obj.course_id

    if not current_course and course_id:
        current_course = Course.query.get(course_id)

    if not current_course and courses:
        current_course = courses[0]
        course_id = current_course.course_id

    # Get lessons for the active course
    lessons = []
    if current_course:
        lessons = Lesson.query.filter_by(
            course_id=current_course.course_id,
            status='Active'
        ).order_by(Lesson.display_order).all()
        if not lessons:
            lessons = Lesson.query.filter_by(
                course_id=current_course.course_id
            ).order_by(Lesson.display_order).all()

    # Determine current active lesson
    current_lesson = None
    if lesson_id:
        current_lesson = Lesson.query.get(lesson_id)
    
    if not current_lesson and lessons:
        current_lesson = lessons[0]

    # Get screens for the active lesson
    screens = []
    if current_lesson:
        screens = Screen.query.filter_by(
            lesson_id=current_lesson.lesson_id,
            status='Active'
        ).order_by(Screen.display_order).all()
        if not screens:
            screens = Screen.query.filter_by(
                lesson_id=current_lesson.lesson_id
            ).order_by(Screen.display_order).all()

    if screen_idx < 0 or (screens and screen_idx >= len(screens)):
        screen_idx = 0

    return render_template(
        'demo/practice.html',
        courses=courses,
        current_course=current_course,
        lessons=lessons,
        current_lesson=current_lesson,
        screens=screens,
        start_screen_idx=screen_idx,
        back_url=back_url,
        portal_name=portal_name,
        user_role=user_role,
        is_demo=True
    )
