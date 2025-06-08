import argparse
from crunevo import create_app, db
from crunevo.models.user import User


def create_user(email: str, username: str, password: str, role: str = "user", app=None):
    app = app or create_app()
    with app.app_context():
        if User.query.filter_by(email=email).first():
            raise ValueError(f"User {email} already exists")
        user = User(username=username, email=email, role=role)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return user


def main() -> None:
    parser = argparse.ArgumentParser(description="Create a user")
    parser.add_argument("email")
    parser.add_argument("username")
    parser.add_argument("password")
    parser.add_argument("--role", default="user")
    args = parser.parse_args()

    try:
        create_user(args.email, args.username, args.password, args.role)
        print(f"Created {args.email} with role {args.role}")
    except Exception as exc:
        print(f"Failed to create user: {exc}")


if __name__ == "__main__":
    main()
