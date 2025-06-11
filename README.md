# Crunevo

Crunevo is a small Flask application. The source code lives in the `crunevo/` folder.

The application now relies on PostgreSQL in production. Set the environment
variable `SQLALCHEMY_DATABASE_URI` with the connection string provided by your
hosting platform (for example Railway).

Define `SQLALCHEMY_DATABASE_URI` directly with your PostgreSQL URL.

ℹ️ Asegúrate de que el archivo `.env` esté en la raíz del proyecto (fuera de
`/crunevo`) para que Flask lo lea correctamente.

## Quick start

1. **Create a virtual environment**

   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

2. **Install dependencies**

   For local development install everything:

   ```bash
   pip install -r requirements.txt
   ```

   For production or Railway use only the core packages:

   ```bash
   pip install -r requirements/requirements-core.txt
   ```

   Optional features such as Cloudinary uploads and PDF previews
   require the extra packages:

   ```bash
   pip install -r requirements/requirements-extras.txt
   ```

3. **Configure la base de datos**

   Exporta `SQLALCHEMY_DATABASE_URI` con la cadena de conexión de PostgreSQL.

4. **Configura FLASK_APP (opcional)**

   Si vas a utilizar la CLI de Flask ejecuta:

   ```bash
   export FLASK_APP=crunevo/app.py
   ```

  Para mayor comodidad el repositorio incluye un archivo `.flaskenv` que
  define `FLASK_APP=run.py`, por lo que podrás iniciar el servidor con
  `flask run` sin necesidad de exportar variables cada vez.

   Los modelos utilizan `from crunevo.extensions import db` para evitar
   errores de importación al ejecutar `flask run`.

5. **Run the application**

   Ejecuta la aplicación con:

   ```bash
   flask run
   ```

   O bien puedes usar:

   ```bash
   python run.py
   ```

6. **Run tests (optional)**

   ```bash
   PYTHONPATH=. pytest -q crunevo/tests
   ```
   Make sure the development requirements are installed first:

   ```bash
   pip install -r requirements/requirements-dev.txt
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
