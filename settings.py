import os

DATABASE_URL = os.getenv("DATABASE_URL")
REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379")
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD", "password123")
