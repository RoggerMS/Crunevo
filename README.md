# Crunevo

Crunevo is a small Flask application. The source code lives in the `crunevo/` folder.

The application now relies on PostgreSQL in production. Set the environment
variable `SQLALCHEMY_DATABASE_URI` with the connection string provided by your
hosting platform (for example Railway).

Define `SQLALCHEMY_DATABASE_URI` directly with your PostgreSQL URL.

## Quick start

1. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

2. **Configure la base de datos**

   Exporta `SQLALCHEMY_DATABASE_URI` con la cadena de conexión de PostgreSQL.

3. **Run the application**

   ```bash
   python run.py
   ```

4. **Run tests (optional)**

   ```bash
   PYTHONPATH=. pytest -q crunevo/tests
   ```
   Make sure the requirements are installed first:

   ```bash
   pip install -r requirements.txt
   ```

## Deployment on Render

Create a `render.yaml` that starts the application with Gunicorn. Provide a
PostgreSQL service and set `SQLALCHEMY_DATABASE_URI` with the connection string.

## Deployment on Railway

For detailed steps see [README_DEPLOY_RAILWAY.md](README_DEPLOY_RAILWAY.md).
En Railway se utiliza el plugin de PostgreSQL y la URL generada se asigna en
`SQLALCHEMY_DATABASE_URI`.

Run the service with Gunicorn just as in Render:

```bash
gunicorn -b 0.0.0.0:$PORT run:app
```



## Docker

You can build and run the application using Docker:

```bash
docker build -t crunevo .
docker run -p 8080:8080 crunevo
```

The container exposes port `8080` by default and starts the app with Gunicorn.
