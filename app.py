from flask import Flask
from config import Config
from database import db
from models import User
from blueprints.auth import auth_bp
from blueprints.admin import admin_bp
from blueprints.student import student_bp

app = Flask(__name__)
app.secret_key = "globalit123"
app.config.from_object(Config)

db.init_app(app)

# Register Blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(student_bp)

with app.app_context():
    db.create_all()

    if User.query.count() == 0:
        admin = User(
            role="Admin",
            username="admin",
            password_hash="admin123",
            status="Active"
        )
        db.session.add(admin)
        db.session.commit()
        print("Default Admin Created")

    print(User.query.all())

if __name__ == "__main__":
    app.run(debug=True)

@app.route('/')
def index():
    return redirect(url_for('auth.login'))
