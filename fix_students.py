from app import app
from database import db
from models import User, Student
from werkzeug.security import generate_password_hash

with app.app_context():
    students = Student.query.all()
    for s in students:
        # Find the user account linked to this student
        user = User.query.filter_by(user_id=s.user_id).first() if hasattr(s, 'user_id') else None
        if not user:
            # Try finding user by username pattern if foreign key differs
            user = User.query.filter_by(username=s.username).first() if hasattr(s, 'username') else User.query.filter(User.username.like(f"%{s.registration_no}%")).first()
        
        if user:
            user.role = 'student'
            user.password_hash = generate_password_hash(str(s.registration_no))
            print(f"Updated password for student username: {user.username} (Password is their Reg No: {s.registration_no})")
            
    db.session.commit()
    print("All student accounts fixed and synced!")