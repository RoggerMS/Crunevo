import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "clave_segura_por_defecto")
    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = os.getenv("DEBUG", "0") == "1"

    NOTE_UPLOAD_FOLDER = os.getenv(
        "NOTE_UPLOAD_FOLDER",
        str(Path(__file__).resolve().parent / "static" / "uploads" / "notes"),
    )
    Path(NOTE_UPLOAD_FOLDER).mkdir(parents=True, exist_ok=True)

    MAX_NOTE_FILE_SIZE_MB = int(os.getenv("MAX_NOTE_FILE_SIZE_MB", "20"))
    MAX_CONTENT_LENGTH = 20 * 1024 * 1024
