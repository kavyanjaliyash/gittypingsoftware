from app import app
from database import db
from models import User
from werkzeug.security import generate_password_hash

with app.app_context():
    admin = User.query.filter_by(username='admin').first()
    if admin:
        admin.password_hash = generate_password_hash('admin123')
        admin.role = 'admin'
        print("Existing admin password reset to 'admin123'")
    else:
        new_admin = User(username='admin', role='admin')
        new_admin.password_hash = generate_password_hash('admin123')
        db.session.add(new_admin)
        print("New admin user created successfully!")
    
    db.session.commit()