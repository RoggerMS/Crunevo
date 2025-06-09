import cloudinary.uploader


def upload_image(file):
    try:
        result = cloudinary.uploader.upload(file)
        return result["secure_url"]
    except Exception as e:
        print("Error al subir imagen a Cloudinary:", e)
        return None
