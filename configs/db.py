from settings import DATABASE_URL

DB_CONFIG = {
    "connections": {
        "default": DATABASE_URL,
    },
    "apps": {
        "models": {
            "models": ["models", "aerich.models"],
            "default_connection": "default",
        }
    }
}