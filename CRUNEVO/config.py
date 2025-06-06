import os
import tempfile
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "clave_segura_por_defecto")

    def _ensure_writable(directory: Path) -> Path:
        try:
            directory.mkdir(parents=True, exist_ok=True)
            test_file = directory / ".write_test"
            with open(test_file, "w"):
                pass
            test_file.unlink()
            return directory
        except OSError:
            fallback = Path(tempfile.gettempdir()) / "crunevo_instance"
            fallback.mkdir(parents=True, exist_ok=True)
            return fallback

    _custom_dir_env = (
        os.getenv("DATABASE_DIR")
        or os.getenv("RAILWAY_VOLUME_MOUNT_PATH")
    )
    if _custom_dir_env:
        _custom_dir = str(_ensure_writable(Path(_custom_dir_env).expanduser()))
    else:
        data_dir = Path("/data")
        if data_dir.is_dir():
            _custom_dir = str(_ensure_writable(data_dir))
        else:
            default_dir = _ensure_writable(
                Path(__file__).resolve().parent / "crunevo" / "instance"
            )
            _custom_dir = str(default_dir)

    env_uri = (
        os.getenv("SQLALCHEMY_DATABASE_URI")
        or os.getenv("DATABASE_URI")
        or os.getenv("DATABASE_URL")
    )
    if env_uri:
        if env_uri.startswith("sqlite:///"):
            db_path = Path(env_uri.replace("sqlite:///", "")).expanduser()
            writable_parent = _ensure_writable(db_path.parent)
            db_path = writable_parent / db_path.name
            env_uri = f"sqlite:///{db_path}"
        SQLALCHEMY_DATABASE_URI = env_uri
    else:
        _default_db = Path(_custom_dir) / "crunevo.sqlite3"
        SQLALCHEMY_DATABASE_URI = f"sqlite:///{_default_db}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = os.getenv("DEBUG", "0") == "1"

    # Provide visibility into the chosen database path. This is useful when the
    # application runs on platforms with read-only source directories as it
    # helps diagnose database initialization errors.
    print(f"Using database URI: {SQLALCHEMY_DATABASE_URI}")
