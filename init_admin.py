"""Create a default admin user if it does not exist."""

from crunevo import create_app, db
from crunevo.models.user import User

ADMIN_EMAIL = "admin@crunevo.com"
ADMIN_USERNAME = "admin"
DEFAULT_PASSWORD = "admin123"

app = create_app()

with app.app_context():
    user = User.query.filter(
        (User.email == ADMIN_EMAIL) | (User.username == ADMIN_USERNAME)
    ).first()
    if user:
        if user.role != "admin":
            user.role = "admin"
            user.set_password(DEFAULT_PASSWORD)
            db.session.commit()
            print(f"Updated existing user {user.email} to admin.")
        else:
            print(f"Admin user already exists: {user.email}")
    else:
        admin = User(
            username=ADMIN_USERNAME,
            email=ADMIN_EMAIL,
            role="admin",
            name="Administrator",
        )
        admin.set_password(DEFAULT_PASSWORD)
        db.session.add(admin)
        db.session.commit()
        print(f"Created admin user: {ADMIN_EMAIL}")
