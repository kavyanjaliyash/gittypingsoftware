"""
Faculty Master Seeding System.
Contains seed data for faculty master records and associated Faculty login accounts.
Preserves exact branch_id foreign key relationships from local database.
Idempotent and safe for production deployments.
"""

import os
import sys
from database import db
from models import Faculty, Branch, User
from werkzeug.security import generate_password_hash

FACULTY_SEED_DATA = [
    {
        "faculty_id": 1,
        "faculty_code": "GIT0001",
        "branch_id": 1,
        "faculty_name": "Chaithra",
        "qualification": "Bcom",
        "experience": "5",
        "mobile": "9945023157",
        "email": "",
        "status": "Active",
        "user": {
            "username": "chaithra1",
            "role": "Faculty",
            "status": "Active"
        }
    },
    {
        "faculty_id": 2,
        "faculty_code": "GIT0002",
        "branch_id": 2,
        "faculty_name": "Meghana M M",
        "qualification": "Bcom",
        "experience": "2",
        "mobile": "8867178897",
        "email": "",
        "status": "Active",
        "user": {
            "username": "Meghanamm",
            "role": "Faculty",
            "status": "Active"
        }
    },
    {
        "faculty_id": 3,
        "faculty_code": "GIT0003",
        "branch_id": 2,
        "faculty_name": "Harshith Kumar P",
        "qualification": "Bcom",
        "experience": "1",
        "mobile": "9845822017",
        "email": "",
        "status": "Active",
        "user": {
            "username": "Harshithp",
            "role": "Faculty",
            "status": "Active"
        }
    }
]

def seed_faculty_data():
    """
    Idempotently seeds faculty master data and required faculty login accounts.
    Checks for existing records before inserting to avoid duplicates or username conflicts.
    """
    inserted_users = 0
    inserted_faculty = 0
    updated_faculty = 0

    seed_password = os.environ.get("FACULTY_SEED_PASSWORD")

    for f_data in FACULTY_SEED_DATA:
        # Check target branch exists by branch_id
        target_branch = db.session.get(Branch, f_data["branch_id"])
        if not target_branch:
            print(f"[Faculty Seed Warning] Branch ID {f_data['branch_id']} not found. Skipping faculty {f_data['faculty_code']}.")
            continue

        u_info = f_data.get("user")
        user_id_to_link = None

        if u_info:
            target_username = u_info["username"]
            # Case-insensitive lookup to avoid username conflict
            existing_user = User.query.filter(db.func.lower(User.username) == target_username.lower()).first()

            if existing_user:
                user_id_to_link = existing_user.user_id
            else:
                if not seed_password:
                    print(f"[Faculty Seed Warning] Cannot create new faculty user '{target_username}': FACULTY_SEED_PASSWORD environment variable is not set. Please configure FACULTY_SEED_PASSWORD in Render.")
                    continue

                new_user = User(
                    role=u_info.get("role", "Faculty"),
                    username=target_username,
                    password_hash=generate_password_hash(seed_password),
                    status=u_info.get("status", "Active")
                )
                db.session.add(new_user)
                db.session.flush()  # Populate new_user.user_id
                user_id_to_link = new_user.user_id
                inserted_users += 1

        # Check if faculty exists by faculty_code or faculty_id
        existing_faculty = Faculty.query.filter_by(faculty_code=f_data["faculty_code"]).first()
        if not existing_faculty and "faculty_id" in f_data:
            existing_faculty = db.session.get(Faculty, f_data["faculty_id"])

        if not existing_faculty:
            faculty = Faculty(
                faculty_id=f_data.get("faculty_id"),
                faculty_code=f_data["faculty_code"],
                branch_id=target_branch.branch_id,
                faculty_name=f_data["faculty_name"],
                qualification=f_data.get("qualification"),
                experience=f_data.get("experience"),
                mobile=f_data.get("mobile"),
                email=f_data.get("email", ""),
                user_id=user_id_to_link,
                status=f_data.get("status", "Active")
            )
            db.session.add(faculty)
            inserted_faculty += 1
        else:
            if user_id_to_link and not existing_faculty.user_id:
                existing_faculty.user_id = user_id_to_link
                updated_faculty += 1

    if inserted_users > 0 or inserted_faculty > 0 or updated_faculty > 0:
        db.session.commit()
        print(f"[Faculty Seed] Seeding complete: {inserted_faculty} faculty created, {inserted_users} faculty users created, {updated_faculty} faculty updated.")
    else:
        print("[Faculty Seed] Faculty master data already present. Skipping seed.")

if __name__ == "__main__":
    from app import app
    with app.app_context():
        seed_faculty_data()
