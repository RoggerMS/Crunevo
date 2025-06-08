# utils/helpers.py
import os
from werkzeug.utils import secure_filename


def guardar_archivo(file, carpeta_destino):
    if file:
        filename = secure_filename(file.filename)
        ruta_completa = os.path.join(carpeta_destino, filename)
        file.save(ruta_completa)
        return filename
    return None


def bytes_a_mb(size_bytes):
    return round(size_bytes / (1024 * 1024), 2)


def resumen_texto(texto, max_palabras=50):
    palabras = texto.split()
    return " ".join(palabras[:max_palabras]) + (
        "..." if len(palabras) > max_palabras else ""
    )
