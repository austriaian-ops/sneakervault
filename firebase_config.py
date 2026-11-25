import os
import json
from pathlib import Path
from functools import lru_cache

from dotenv import load_dotenv

import firebase_admin
from firebase_admin import credentials, firestore


BASE_DIR = Path(__file__).resolve().parent

load_dotenv(BASE_DIR / ".env", override=False)


@lru_cache(maxsize=1)
def get_db():

    try:

        if not firebase_admin._apps:

            firebase_json = os.getenv(
                "FIREBASE_SERVICE_ACCOUNT"
            )

            if firebase_json:

                # Vercel deployment
                service_account = json.loads(firebase_json)

                cred = credentials.Certificate(
                    service_account
                )

            else:

                # Local PyCharm development
                key_file = os.getenv(
                    "GOOGLE_APPLICATION_CREDENTIALS",
                    "ServiceAccountKey.json"
                )

                key_path = Path(key_file)

                if not key_path.is_absolute():
                    key_path = BASE_DIR / key_path

                if not key_path.is_file():
                    raise FileNotFoundError(
                        f"Firebase key not found: {key_path}"
                    )

                cred = credentials.Certificate(
                    str(key_path)
                )

            firebase_admin.initialize_app(cred)

        db = firestore.client()

        print("Firebase initialized successfully!")
        print("Firebase Project ID:", db.project)

        return db

    except Exception as error:

        print("FIREBASE ERROR:", str(error))

        raise
