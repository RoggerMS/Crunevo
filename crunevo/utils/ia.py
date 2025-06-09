import os
import requests
from flask_login import current_user


def fetch_cohere_advice() -> str:
    """Return a short recommendation using Cohere or fallback text."""
    api_key = os.getenv("COHERE_API_KEY")
    if not api_key:
        return (
            "Los apuntes de Álgebra son los más descargados hoy. "
            "¡Puedes subir uno y ganar +8 créditos!"
        )

    prompt = (
        "Qué apunte debería subir un estudiante de "
        f"{current_user.career or 'carrera'} en Perú para recibir más descargas?"
    )
    data = {"model": "command", "prompt": prompt, "max_tokens": 60}
    headers = {"Authorization": f"Bearer {api_key}"}

    try:
        response = requests.post(
            "https://api.cohere.ai/generate",
            json=data,
            headers=headers,
            timeout=10,
        )
        response.raise_for_status()
        text = response.json().get("generations", [{}])[0].get("text", "")
        return text.strip() or (
            "Comparte apuntes populares de tu carrera para ganar más créditos."
        )
    except Exception:
        return "Comparte apuntes populares de tu carrera para ganar más créditos."
