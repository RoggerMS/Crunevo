import importlib


def test_env_loaded_correctly(monkeypatch):
    monkeypatch.setenv("DATABASE_URL", "sqlite:///memory")
    monkeypatch.setenv("SECRET_KEY", "test_secret")
    monkeypatch.delenv("SQLALCHEMY_DATABASE_URI", raising=False)
    import crunevo.config as config_module

    cfg = importlib.reload(config_module)
    assert cfg.Config.SQLALCHEMY_DATABASE_URI == "sqlite:///memory"
    assert cfg.Config.SECRET_KEY == "test_secret"
