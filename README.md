# Crunevo

Crunevo is a small Flask application. The repository contains the `CRUNEVO` folder with the application and tests. It uses SQLite by default so it works out of the box with almost no configuration.

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

## Quick start

1. **Install dependencies**

   ```bash
   pip install -r CRUNEVO/requirements.txt
   ```

2. **Choose a writable directory for the database**

   Set the environment variable `DATABASE_DIR` (or `SQLALCHEMY_DATABASE_URI`) to a directory where the application can create the `crunevo.sqlite3` file. For example:

   ```bash
   export DATABASE_DIR=/data
   ```

   The directory must exist and be writable. You can also set `SQLALCHEMY_DATABASE_URI` directly if you prefer.

3. **Run the application**

   ```bash
   python CRUNEVO/run.py
   ```

4. **Run tests (optional)**

   ```bash
   pytest -q CRUNEVO/tests
   ```

## Deployment on Render

The repository includes a `render.yaml` file that builds the project and starts the application with Gunicorn. A persistent disk is mounted at `/data` and the environment variable `DATABASE_DIR` is set to that path so the SQLite database can be created. Gunicorn is listed in `CRUNEVO/requirements.txt` so it is installed automatically during the build step.

1. Push the repository to a new Render web service.
2. Make sure the service has a persistent disk attached at `/data`.
3. Deploy; Render will install the requirements and start the app using the command defined in `render.yaml`.

