# Crunevo

Crunevo is a small Flask application. The repository contains the `CRUNEVO` folder with the application and tests. It uses SQLite by default so it works out of the box with almost no configuration.

The deployment on platforms such as Render requires that the SQLite database is
stored on a writable disk. If the app fails with
`sqlite3.OperationalError: unable to open database file` it usually means the
application does not have permission to create the database file. Make sure a
persistent disk is mounted (for example at `/data`) or set a custom writable
location with the variables described below.  The application prints the final
database URI on startup, so you can verify that it points to a writable
directory.

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
   Make sure the requirements are installed first:

   ```bash
   pip install -r CRUNEVO/requirements.txt
   ```

## Deployment on Render

For deployments on **Render**, create a `render.yaml` file that builds the
project and starts the application with Gunicorn. The file should mount a
persistent disk at `/data` and set the environment variable `DATABASE_DIR` to
that path so the SQLite database can be created. Gunicorn is listed in
`CRUNEVO/requirements.txt` so it is installed automatically during the build
step.

1. Push the repository to a new Render web service.
2. Make sure the service has a persistent disk attached at `/data`.
3. Deploy; Render will install the requirements and start the app using the
   command defined in `render.yaml`.

## Deployment on Railway

If you move the project to **Railway**, attach a volume so the SQLite database
can be stored on a writable filesystem. Set the mount path of that volume using
the `RAILWAY_VOLUME_MOUNT_PATH` environment variable or define `DATABASE_DIR`
directly. The application checks those variables on startup and creates the
database there.

Run the service with Gunicorn just as in Render:

```bash
gunicorn -b 0.0.0.0:$PORT CRUNEVO.run:app
```

Without a volume the application falls back to a temporary directory and the
data will be lost on redeploys.

