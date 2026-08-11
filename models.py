from database import db

class User(db.Model):
    __tablename__ = "users"
    user_id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.String(20), nullable=False)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    status = db.Column(db.String(20), default="Active")

class Branch(db.Model):
    __tablename__ = "branches"
    branch_id = db.Column(db.Integer, primary_key=True)
    branch_name = db.Column(db.String(100), nullable=False)
    branch_code = db.Column(db.String(20), unique=True, nullable=False)
    address = db.Column(db.Text)
    phone = db.Column(db.String(15))
    email = db.Column(db.String(100))
    status = db.Column(db.String(20), default="Active")
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=True)

    user = db.relationship("User", backref="branches")

class Faculty(db.Model):
    __tablename__ = "faculty"
    faculty_id = db.Column(db.Integer, primary_key=True)
    faculty_code = db.Column(db.String(20), unique=True)
    branch_id = db.Column(db.Integer, db.ForeignKey("branches.branch_id"), nullable=False)
    faculty_name = db.Column(db.String(100), nullable=False)
    qualification = db.Column(db.String(100))
    experience = db.Column(db.String(50))
    mobile = db.Column(db.String(15))
    email = db.Column(db.String(100))
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)
    status = db.Column(db.String(20), default="Active")

    branch = db.relationship("Branch", backref="faculties")
    user = db.relationship("User", backref="faculties")

class Student(db.Model):
    __tablename__ = "students"
    student_id = db.Column(db.Integer, primary_key=True)
    registration_no = db.Column(db.String(30), unique=True, nullable=False)
    student_name = db.Column(db.String(100), nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    dob = db.Column(db.Date)
    mobile = db.Column(db.String(15), nullable=False)
    email = db.Column(db.String(100))
    branch_id = db.Column(db.Integer, db.ForeignKey("branches.branch_id"), nullable=False)
    course = db.Column(db.String(100), nullable=False)
    faculty_id = db.Column(db.Integer, db.ForeignKey("faculty.faculty_id"), nullable=False)
    english_wpm = db.Column(db.Integer, default=0)
    kannada_wpm = db.Column(db.Integer, default=0)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)
    status = db.Column(db.String(20), default="Active")

    branch = db.relationship("Branch", backref="students")
    faculty = db.relationship("Faculty", backref="students")
    user = db.relationship("User", backref="students")

class Course(db.Model):
    __tablename__ = "courses"
    course_id = db.Column(db.Integer, primary_key=True)
    course_name = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(20), default="Active")
    lessons = db.relationship("Lesson", backref="course", order_by="Lesson.display_order")

class Lesson(db.Model):
    __tablename__ = "lessons"
    lesson_id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey("courses.course_id"), nullable=False)
    lesson_title = db.Column(db.String(200), nullable=False)
    lesson_description = db.Column(db.Text)
    chapter = db.Column(db.String(100), default="Beginner") # 'Beginner', 'Intermediate', 'Advanced'
    display_order = db.Column(db.Integer, default=1)
    status = db.Column(db.String(20), default="Active")

class Screen(db.Model):
    __tablename__ = "lesson_screens"
    screen_id = db.Column(db.Integer, primary_key=True)
    lesson_id = db.Column(db.Integer, db.ForeignKey("lessons.lesson_id"), nullable=False)
    screen_title = db.Column(db.String(200), nullable=False)
    screen_content = db.Column(db.Text, nullable=False)
    screen_type = db.Column(db.String(50), default="block") # 'block', 'waterfall', 'jump'
    display_order = db.Column(db.Integer, default=1)
    status = db.Column(db.String(20), default="Active")
    
    lesson = db.relationship("Lesson", backref="screens")

class StudentProgress(db.Model):
    __tablename__ = "student_progress"
    progress_id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("students.student_id"))
    lesson_id = db.Column(db.Integer, db.ForeignKey("lessons.lesson_id"))
    wpm = db.Column(db.Integer)
    accuracy = db.Column(db.Float)
    mistakes = db.Column(db.Integer)
    time_taken = db.Column(db.Integer)
    completed_on = db.Column(db.DateTime)
    status = db.Column(db.String(20))

class TypingGame(db.Model):
    __tablename__ = "typing_games"
    game_id = db.Column(db.Integer, primary_key=True)
    game_name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(100), default="Speed & Accuracy")
    difficulty = db.Column(db.String(50), default="Medium")
    status = db.Column(db.String(20), default="Active")