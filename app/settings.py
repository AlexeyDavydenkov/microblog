import os

# Определяем текущее окружение
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")

if ENVIRONMENT == "testing":
    DATABASE_URL = "sqlite:///:memory:"
else:
    DATABASE_URL = "postgresql://postgres:postgres@db/microblog"
