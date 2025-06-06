import os
import tempfile
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "clave_segura_por_defecto")

    _custom_dir = os.getenv("DATABASE_DIR")
    if _custom_dir:
        Path(_custom_dir).mkdir(parents=True, exist_ok=True)
    else:
        default_dir = Path(__file__).resolve().parent / "crunevo" / "instance"
        try:
            default_dir.mkdir(parents=True, exist_ok=True)
        except OSError:
            temp_dir = Path(tempfile.gettempdir()) / "crunevo_instance"
            temp_dir.mkdir(parents=True, exist_ok=True)
            default_dir = temp_dir
        _custom_dir = str(default_dir)

    _default_db = Path(_custom_dir) / "crunevo.sqlite3"

    SQLALCHEMY_DATABASE_URI = os.getenv(
        "SQLALCHEMY_DATABASE_URI", f"sqlite:///{_default_db}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = os.getenv("DEBUG", "0") == "1"
