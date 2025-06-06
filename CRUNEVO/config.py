import os
import tempfile
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "clave_segura_por_defecto")

    _custom_dir = os.getenv("DATABASE_DIR")
    if not _custom_dir:
        default_dir = Path(__file__).resolve().parent / "crunevo" / "instance"
        try:
            default_dir.mkdir(parents=True, exist_ok=True)
        except OSError:
            temp_dir = Path(tempfile.gettempdir()) / "crunevo_instance"
            temp_dir.mkdir(parents=True, exist_ok=True)
            default_dir = temp_dir
        _custom_dir = str(default_dir)
    else:
        Path(_custom_dir).mkdir(parents=True, exist_ok=True)

    env_uri = os.getenv("SQLALCHEMY_DATABASE_URI")
    if env_uri:
        if env_uri.startswith("sqlite:///"):
            db_path = Path(env_uri.replace("sqlite:///", ""))
            db_path.parent.mkdir(parents=True, exist_ok=True)
        SQLALCHEMY_DATABASE_URI = env_uri
    else:
        _default_db = Path(_custom_dir) / "crunevo.sqlite3"
        SQLALCHEMY_DATABASE_URI = f"sqlite:///{_default_db}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = os.getenv("DEBUG", "0") == "1"
