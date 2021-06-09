import os

DB_CONFIG = {
    "connections": {
        "default": os.environ.get("DATABASE_URL"),
        "test": "sqlite://:memory:"
    },
    "apps": {
        "models": {
            "models": ["models"],
            "default_connection": "default",
        }
    }
}