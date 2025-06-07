"""Utility functions for working with file uploads and Amazon S3."""
import os
from typing import Optional
from flask import current_app, flash, url_for
from werkzeug.utils import secure_filename
from botocore.exceptions import NoCredentialsError, ClientError
import boto3

# Allowed extensions for note uploads
ALLOWED_EXTENSIONS = {"pdf", "png", "jpg", "jpeg", "doc", "docx", "txt"}


def allowed_file(filename: str) -> bool:
    """Return True if the filename has an allowed extension."""
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def upload_file_to_s3(file, bucket_name: str, region: Optional[str] = None, acl: str = "public-read") -> Optional[str]:
    """Upload the given file object to an S3 bucket.

    Parameters
    ----------
    file: FileStorage
        File object received from a Flask request.
    bucket_name: str
        Target S3 bucket.
    region: Optional[str]
        AWS region of the bucket. If not provided, defaults to ``us-east-1``.
    acl: str
        Access control list for the object, defaults to ``public-read``.

    Returns
    -------
    Optional[str]
        Public URL for the uploaded file or ``None`` if an error occurred.
    """
    region = region or os.environ.get("AWS_REGION", "us-east-1")
    s3_client = boto3.client("s3", region_name=region)
    filename = secure_filename(file.filename)
    try:
        s3_client.upload_fileobj(
            file,
            bucket_name,
            filename,
            ExtraArgs={
                "ACL": acl,
                "ContentType": file.content_type,
            },
        )
        base_url = f"https://{bucket_name}.s3.{region}.amazonaws.com/"
        return f"{base_url}{filename}"
    except (NoCredentialsError, ClientError, Exception) as e:
        flash("Ocurri\u00f3 un error al subir el archivo.", "danger")
        current_app.logger.error(f"Error al subir archivo a S3: {e}", exc_info=True)
        return None


def save_file_local(file, upload_folder: str) -> Optional[str]:
    """Save the given file locally inside the static folder and return its URL."""
    try:
        os.makedirs(upload_folder, exist_ok=True)
        filename = secure_filename(file.filename)
        file_path = os.path.join(upload_folder, filename)
        file.save(file_path)
        relative = os.path.relpath(file_path, current_app.static_folder)
        return url_for("static", filename=relative)
    except Exception as e:
        flash("Ocurri\u00f3 un error al guardar el archivo.", "danger")
        current_app.logger.error(f"Error al guardar archivo local: {e}", exc_info=True)
        return None
