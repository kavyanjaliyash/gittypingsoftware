"""
Branch Master Seeding System.
Contains seed data for branch master records (Admin Branch, Hoskote Branch) and associated Branch login accounts.
Idempotent and safe for production deployments.
"""

import os
import sys
from database import db
from models import Branch, User
from werkzeug.security import generate_password_hash

BRANCHES_SEED_DATA = [
    {
        "branch_id": 1,
        "branch_name": "Admin Branch",
        "branch_code": "Admin01",
        "address": None,
        "phone": "9071717162",
        "email": "",
        "status": "Active",
        "user": {
            "username": "Admin01",
            "role": "Branch",
            "status": "Active"
        }
    },
    {
        "branch_id": 2,
        "branch_name": "Hoskote Branch",
        "branch_code": "HSKBranch01",
        "address": None,
        "phone": "",
        "email": "",
        "status": "Active",
        "user": {
            "username": "Hoskotebranch01",
            "role": "Branch",
            "status": "Active"
        }
    }
]

def seed_branches_data():
    """
    Idempotently seeds branch master data and required branch login accounts.
    Checks for existing records before inserting to avoid duplicates or username conflicts.
    """
    inserted_users = 0
    inserted_branches = 0
    updated_branches = 0

    default_password = os.environ.get("BRANCH_SEED_PASSWORD", "Admin@123")

    for b_data in BRANCHES_SEED_DATA:
        u_info = b_data.get("user")
        user_id_to_link = None

        if u_info:
            target_username = u_info["username"]
            # Case-insensitive lookup to avoid username conflict
            existing_user = User.query.filter(db.func.lower(User.username) == target_username.lower()).first()

            if existing_user:
                user_id_to_link = existing_user.user_id
            else:
                new_user = User(
                    role=u_info.get("role", "Branch"),
                    username=target_username,
                    password_hash=generate_password_hash(default_password),
                    status=u_info.get("status", "Active")
                )
                db.session.add(new_user)
                db.session.flush()  # Populate new_user.user_id
                user_id_to_link = new_user.user_id
                inserted_users += 1

        # Check if branch exists by branch_code or branch_id
        existing_branch = Branch.query.filter_by(branch_code=b_data["branch_code"]).first()
        if not existing_branch and "branch_id" in b_data:
            existing_branch = db.session.get(Branch, b_data["branch_id"])

        if not existing_branch:
            branch = Branch(
                branch_id=b_data.get("branch_id"),
                branch_name=b_data["branch_name"],
                branch_code=b_data["branch_code"],
                address=b_data.get("address"),
                phone=b_data.get("phone", ""),
                email=b_data.get("email", ""),
                status=b_data.get("status", "Active"),
                user_id=user_id_to_link
            )
            db.session.add(branch)
            inserted_branches += 1
        else:
            if user_id_to_link and not existing_branch.user_id:
                existing_branch.user_id = user_id_to_link
                updated_branches += 1

    if inserted_users > 0 or inserted_branches > 0 or updated_branches > 0:
        db.session.commit()
        print(f"[Branch Seed] Seeding complete: {inserted_branches} branches created, {inserted_users} branch users created, {updated_branches} branches updated.")
    else:
        print("[Branch Seed] Branch master data already present. Skipping seed.")

if __name__ == "__main__":
    from app import app
    with app.app_context():
        seed_branches_data()
