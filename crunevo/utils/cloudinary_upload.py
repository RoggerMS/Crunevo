try:
    import cloudinary.uploader
except ImportError:  # pragma: no cover - optional dependency
    cloudinary = None


def upload_image(file):
    """Return the uploaded image URL or None if Cloudinary is unavailable."""
    if not cloudinary:
        print("Cloudinary no está instalado")
        return None
    try:
        result = cloudinary.uploader.upload(file)
        return result.get("secure_url")
    except Exception as e:  # pragma: no cover - network/dependency issues
        print("Error al subir imagen a Cloudinary:", e)
        return None
