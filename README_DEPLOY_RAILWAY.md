# Despliegue de Crunevo en Railway

Sigue estos pasos para ejecutar la aplicación usando Railway y un volumen para SQLite.

## 1. Preparación del repositorio

Elimina `render.yaml` para usar únicamente Railway:

```bash
rm render.yaml
git rm render.yaml
git commit -m "Remove render.yaml - using Railway only"
git push
```

## 2. Configuración en Railway

1. Crea un proyecto en Railway y vincula tu repositorio.
2. En **Settings** define los comandos:
   - **Start Command**:
     ```bash
     gunicorn -b 0.0.0.0:$PORT CRUNEVO.run:app
     ```
   - **Build Command** (si no detecta `requirements.txt` automáticamente):
     ```bash
     pip install -r requirements.txt
     ```
3. Define una de las variables de entorno para indicar la ruta del volumen:
   - `RAILWAY_VOLUME_MOUNT_PATH=/mnt/data`
   - o `DATABASE_DIR=/mnt/data`
4. En **Volumes** crea un volumen de al menos 1GB y móntalo en `/mnt/data`.

Con esta configuración, Railway instalará las dependencias y ejecutará la aplicación con Gunicorn usando el puerto proporcionado por la plataforma.
