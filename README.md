# Crunevo

Crunevo is a small Flask application. The repository contains the `CRUNEVO` folder with the application and tests.

The deployment on platforms such as Render requires that the SQLite database is
stored on a writable disk. If the app fails with
`sqlite3.OperationalError: unable to open database file` it usually means the
application does not have permission to create the database file. Make sure a
persistent disk is mounted (for example at `/data`) or set a custom writable
location with the variables described below.

Set the environment variable `DATABASE_DIR` (or `SQLALCHEMY_DATABASE_URI`) to a
writable directory. Paths containing `~` are expanded automatically.

If `DATABASE_DIR` is not defined, the configuration now checks whether `/data`
exists and is writable (this is where a Render persistent disk is mounted). If
it is, that path is used automatically. The provided `render.yaml` mounts a
persistent disk at `/data` and sets `DATABASE_DIR=/data`, so deployment works
out of the box.

Run tests with:

```bash
pytest -q CRUNEVO/tests
```
