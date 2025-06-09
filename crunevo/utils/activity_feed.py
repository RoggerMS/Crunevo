# -*- coding: utf-8 -*-
"""Utility functions for building user activity feeds."""

from typing import List, Dict


def build_user_activity(user) -> List[Dict[str, object]]:
    """Return a sorted list of activity events for the given user."""
    events = []

    for note in getattr(user, "notes", []):
        events.append(
            {
                "timestamp": note.upload_date,
                "message": f'📤 Subiste el apunte "{note.title}"',
            }
        )
        if note.downloads_count:
            events.append(
                {
                    "timestamp": note.upload_date,
                    "message": f'⬇️ Tu apunte "{note.title}" fue descargado {note.downloads_count} veces',
                }
            )

    for r in getattr(user, "respuestas", []):
        if r.pregunta:
            events.append(
                {
                    "timestamp": r.fecha,
                    "message": f'💬 Respondiste a la pregunta "{r.pregunta.titulo}"',
                }
            )

    for p in getattr(user, "posts", []):
        events.append(
            {"timestamp": p.timestamp, "message": "📢 Publicaste una actualización"}
        )

    events.sort(key=lambda e: e["timestamp"], reverse=True)
    return events
