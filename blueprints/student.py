from flask import Blueprint, render_template, session, redirect, url_for, request, jsonify
from database import db
from models import Student, Course, Lesson, Screen, User, StudentProgress
from datetime import datetime
import unicodedata

student_bp = Blueprint('student', __name__, url_prefix='/student')

@student_bp.route('/dashboard')
def dashboard():
    if 'user_id' not in session or session.get('role') != 'student':
        return redirect(url_for('auth.login'))
    
    student = Student.query.filter_by(user_id=session['user_id']).first()
    courses = Course.query.filter_by(status='Active').all()
    
    completed_progress = StudentProgress.query.filter_by(
        student_id=student.student_id, 
        status='Completed'
    ).all() if student else []

    progress_map = {p.lesson_id: p for p in completed_progress}
    completed_lesson_ids = [p.lesson_id for p in completed_progress]

    course_stats = {}
    for c in courses:
        active_lessons = [l for l in c.lessons if len(l.screens) > 0]
        total_lessons = len(active_lessons) if active_lessons else len(c.lessons)
        completed_count = sum(1 for l in (active_lessons or c.lessons) if l.lesson_id in completed_lesson_ids)
        pct = round((completed_count / total_lessons) * 100) if total_lessons > 0 else 100
        is_completed = (pct == 100)
        course_stats[c.course_id] = {
            'total_lessons': len(c.lessons),
            'completed_count': completed_count,
            'pct': pct,
            'is_completed': is_completed
        }

    return render_template(
        'student/dashboard.html', 
        student=student, 
        courses=courses, 
        completed_lesson_ids=completed_lesson_ids,
        progress_map=progress_map,
        course_stats=course_stats
    )

@student_bp.route('/certificate/<int:course_id>')
@student_bp.route('/certificate')
def print_certificate(course_id=1):
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    user_role = session.get('role', '')
    student_id_arg = request.args.get('student_id')

    if student_id_arg:
        student = Student.query.get(student_id_arg)
    else:
        student = Student.query.filter_by(user_id=session['user_id']).first()

    if not student:
        student = Student.query.first()

    course = Course.query.get(course_id) or Course.query.first()
    completion_date = datetime.now().strftime("%B %d, %Y")

    if user_role in ['branch', 'branch_admin', 'branch admin'] or user_role != 'student':
        back_url = url_for('branch.student_details', student_id=student.student_id, subtab='achievements')
    else:
        back_url = url_for('student.dashboard', subtab='achievements')

    return render_template(
        'student/certificate.html',
        student=student,
        course=course,
        avg_wpm=student.english_wpm or 20,
        avg_accuracy=98,
        completion_date=completion_date,
        back_url=back_url
    )

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
    
    saved_screen_idx = session.get(f'student_{student.student_id}_lesson_{lesson_id}_screen', 0) if student else 0
    if saved_screen_idx >= len(screens):
        saved_screen_idx = max(0, len(screens) - 1)
    
    return render_template(
        'student/lesson.html', 
        student=student, 
        lesson=lesson, 
        screens=screens,
        saved_screen_idx=saved_screen_idx
    )

@student_bp.route('/lesson/<int:lesson_id>/save_screen_progress', methods=['POST'])
def save_screen_progress(lesson_id):
    if 'user_id' not in session or session.get('role') != 'student':
        return jsonify({'success': False, 'error': 'Unauthorized'}), 401
    
    student = Student.query.filter_by(user_id=session['user_id']).first()
    if not student:
        return jsonify({'success': False, 'error': 'Student not found'}), 404
        
    data = request.get_json(silent=True) or request.form
    screen_index = int(data.get('screen_index', 0))
    wpm = int(data.get('wpm', 0))
    accuracy = float(data.get('accuracy', 100.0))
    mistakes = int(data.get('mistakes', 0))
    seconds = int(data.get('seconds', 0))
    
    next_screen_idx = screen_index + 1
    session[f'student_{student.student_id}_lesson_{lesson_id}_screen'] = next_screen_idx
    session.modified = True
    
    # Save/update progress record in DB
    progress = StudentProgress.query.filter_by(
        student_id=student.student_id, 
        lesson_id=lesson_id
    ).first()
    
    if not progress:
        progress = StudentProgress(
            student_id=student.student_id,
            lesson_id=lesson_id,
            wpm=wpm,
            accuracy=accuracy,
            mistakes=mistakes,
            time_taken=seconds,
            completed_on=datetime.now(),
            status='In Progress'
        )
        db.session.add(progress)
    elif progress.status != 'Completed':
        progress.wpm = wpm
        progress.accuracy = accuracy
        progress.mistakes = mistakes
        progress.time_taken = seconds
        progress.status = 'In Progress'
        
    db.session.commit()
    
    return jsonify({'success': True, 'next_screen_idx': next_screen_idx})

@student_bp.route('/lesson/<int:lesson_id>/complete', methods=['POST'])
def complete_lesson(lesson_id):
    if 'user_id' not in session or session.get('role') != 'student':
        return redirect(url_for('auth.login'))
    
    student = Student.query.filter_by(user_id=session['user_id']).first()
    lesson = Lesson.query.get_or_404(lesson_id)
    
    wpm = int(request.form.get('wpm', 0))
    mistakes = int(request.form.get('mistakes', 0))
    seconds = int(request.form.get('seconds', 0))

    if student:
        # Clear in-progress session key for this lesson
        session.pop(f'student_{student.student_id}_lesson_{lesson_id}_screen', None)
        session.modified = True

        # Save or update progress record in DB
        progress = StudentProgress.query.filter_by(
            student_id=student.student_id, 
            lesson_id=lesson_id
        ).first()

        if not progress:
            progress = StudentProgress(
                student_id=student.student_id,
                lesson_id=lesson_id,
                wpm=wpm,
                accuracy=100.0,
                mistakes=mistakes,
                time_taken=seconds,
                completed_on=datetime.now(),
                status='Completed'
            )
            db.session.add(progress)
        else:
            progress.wpm = wpm
            progress.mistakes = mistakes
            progress.time_taken = seconds
            progress.completed_on = datetime.now()
            progress.status = 'Completed'

        db.session.flush()

        # Recalculate average WPM across all completed lessons for English and Kannada
        all_progress = StudentProgress.query.filter_by(
            student_id=student.student_id, 
            status='Completed'
        ).all()

        eng_wpms = []
        kan_wpms = []

        for p in all_progress:
            if p.wpm is not None and p.wpm > 0:
                l = Lesson.query.get(p.lesson_id)
                if l and l.course:
                    if 'Kannada' in l.course.course_name:
                        kan_wpms.append(p.wpm)
                    else:
                        eng_wpms.append(p.wpm)

        student.english_wpm = round(sum(eng_wpms) / len(eng_wpms)) if eng_wpms else 0
        student.kannada_wpm = round(sum(kan_wpms) / len(kan_wpms)) if kan_wpms else 0

        db.session.commit()
    
    next_lesson = Lesson.query.filter(
        Lesson.course_id == lesson.course_id, 
        Lesson.display_order > lesson.display_order
    ).order_by(Lesson.display_order.asc()).first()
    
    # Calculate accuracy and stars based on errors & speed
    accuracy = 100
    if mistakes > 0:
        accuracy = max(0, min(100, round(100 - (mistakes * 4))))

    if mistakes == 0 and wpm >= 10:
        stars = 3
    elif mistakes <= 2:
        stars = 2
    else:
        stars = 1

    return render_template(
        'student/completion.html', 
        student=student, 
        lesson=lesson, 
        wpm=wpm, 
        mistakes=mistakes, 
        seconds=seconds, 
        accuracy=accuracy,
        stars=stars,
        next_lesson=next_lesson
    )