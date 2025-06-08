import os

os.environ.setdefault("DATABASE_URL", "sqlite:///test.db")
os.environ.setdefault("SECRET_KEY", "testing-secret")
os.environ.pop("SQLALCHEMY_DATABASE_URI", None)
