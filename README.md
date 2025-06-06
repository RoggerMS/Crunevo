# Crunevo

Crunevo is a small Flask application. The repository contains the `CRUNEVO` folder with the application and tests.

The deployment on platforms such as Render requires that the SQLite database is
stored on a writable disk. If the app fails with
`sqlite3.OperationalError: unable to open database file` ensure that the
application can write to the configured path.

Set the environment variable `DATABASE_DIR` (or `SQLALCHEMY_DATABASE_URI`) to a
writable directory. Paths containing `~` are expanded automatically.

The provided `render.yaml` already mounts a persistent disk at `/data` and sets `DATABASE_DIR=/data` so a simple deployment works out of the box.

Run tests with:

```bash
pytest -q CRUNEVO/tests
```
