import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "clave_segura_por_defecto")

    _custom_dir = os.getenv("DATABASE_DIR")
    if _custom_dir:
        os.makedirs(_custom_dir, exist_ok=True)
        _default_db = os.path.join(_custom_dir, "crunevo.sqlite3")
    else:
        _instance_dir = os.path.join(os.getcwd(), "instance")
        os.makedirs(_instance_dir, exist_ok=True)
        _default_db = os.path.join(_instance_dir, "crunevo.sqlite3")

    SQLALCHEMY_DATABASE_URI = os.getenv(
        "SQLALCHEMY_DATABASE_URI", f"sqlite:///{_default_db}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = os.getenv("DEBUG", "0") == "1"
