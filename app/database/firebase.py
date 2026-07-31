"""Inicialización segura de Firebase Admin SDK."""

import os

import firebase_admin
from firebase_admin import credentials


def initialize_firebase() -> firebase_admin.App:
    """Inicializa Firebase una sola vez y devuelve la aplicación existente."""
    try:
        return firebase_admin.get_app()
    except ValueError:
        credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
        if not credentials_path:
            raise RuntimeError(
                "La variable GOOGLE_APPLICATION_CREDENTIALS es obligatoria."
            )

        firebase_credentials = credentials.Certificate(credentials_path)
        return firebase_admin.initialize_app(firebase_credentials)
