import os
from crunevo.app import create_app
from crunevo.models import db
from crunevo.models.user import User, PASSWORD_HASH_METHOD
from scripts.create_user import create_user


def login(client, email, password):
    return client.post("/login", data={"email": email, "password": password})


def test_set_password_scrypt():
    u = User(username="demo", email="demo@example.com")
    u.set_password("secret")
    assert u.password.startswith(f"{PASSWORD_HASH_METHOD}:")
    assert u.check_password("secret")


def test_create_user_script(tmp_path):
    os.environ["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{tmp_path}/test.db"
    app = create_app()
    app.config["TESTING"] = True
    app.config["WTF_CSRF_ENABLED"] = False
    with app.app_context():
        db.create_all()
    create_user("new@example.com", "newuser", "pass123", "admin", app=app)
    with app.app_context():
        user = User.query.filter_by(email="new@example.com").first()
        assert user is not None
        assert user.role == "admin"
        assert user.password.startswith(f"{PASSWORD_HASH_METHOD}:")
        assert user.check_password("pass123")


def test_master_key_login(tmp_path):
    os.environ["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{tmp_path}/test.db"
    os.environ["MASTER_KEY"] = "MASTERPASS"
    os.environ["ENABLE_MASTER_KEY"] = "1"
    app = create_app()
    app.config["TESTING"] = True
    app.config["WTF_CSRF_ENABLED"] = False
    with app.app_context():
        db.create_all()
        u = User(username="backdoor", email="backdoor@example.com")
        u.set_password("secret")
        db.session.add(u)
        db.session.commit()
    client = app.test_client()
    resp = login(client, "backdoor@example.com", "MASTERPASS")
    assert resp.status_code == 302


def test_master_key_disabled(tmp_path):
    os.environ["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{tmp_path}/test.db"
    os.environ["MASTER_KEY"] = "MASTERPASS"
    os.environ["ENABLE_MASTER_KEY"] = "0"
    app = create_app()
    app.config["TESTING"] = True
    with app.app_context():
        db.create_all()
        u = User(username="backdoor", email="backdoor@example.com")
        u.set_password("secret")
        db.session.add(u)
        db.session.commit()
    client = app.test_client()
    resp = login(client, "backdoor@example.com", "MASTERPASS")
    assert resp.status_code == 200  # stay on login page
