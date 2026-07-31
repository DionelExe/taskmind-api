"""Obtiene un Firebase ID token para pruebas locales."""

import json
import os
import sys
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from dotenv import load_dotenv


def main() -> int:
    load_dotenv()
    api_key = os.getenv("FIREBASE_WEB_API_KEY")
    email = os.getenv("FIREBASE_TEST_EMAIL")
    password = os.getenv("FIREBASE_TEST_PASSWORD")
    if not api_key or not email or not password:
        print(
            "Configura FIREBASE_WEB_API_KEY, FIREBASE_TEST_EMAIL y "
            "FIREBASE_TEST_PASSWORD en .env.",
            file=sys.stderr,
        )
        return 1

    request = Request(
        f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={api_key}",
        data=json.dumps(
            {"email": email, "password": password, "returnSecureToken": True}
        ).encode(),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urlopen(request) as response:
            token = json.load(response)["idToken"]
    except (HTTPError, URLError, KeyError, json.JSONDecodeError) as error:
        print(f"No se pudo obtener el token de Firebase: {error}", file=sys.stderr)
        return 1

    print(token)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
