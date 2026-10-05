"""Настройки для pytest. Значения генерируются при запуске, секретов в коде нет."""

import os

from django.core.management.utils import get_random_secret_key

os.environ.setdefault("DJANGO_SECRET_KEY", get_random_secret_key())
os.environ.setdefault("ADMIN_URL", "test-admin-path/")

from .base import *  # noqa: F403

DEBUG = False
ALLOWED_HOSTS = ["testserver"]

# На этапе 1 моделей нет — достаточно SQLite в памяти, Postgres для тестов не нужен.
DATABASES = {"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": ":memory:"}}

PASSWORD_HASHERS = ["django.contrib.auth.hashers.MD5PasswordHasher"]
