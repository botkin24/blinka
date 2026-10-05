"""Боевые настройки. Раздел 11.3 ТЗ; `manage.py check --deploy` — без предупреждений."""

from .base import *  # noqa: F403

DEBUG = False
ALLOWED_HOSTS = ["xn--80abvidn.xn--p1ai", "www.xn--80abvidn.xn--p1ai"]
CSRF_TRUSTED_ORIGINS = ["https://xn--80abvidn.xn--p1ai"]

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# HSTS поэтапно (11.3): 1 день → 30 дней → 1 год.
SECURE_HSTS_SECONDS = 24 * 3600
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = False

SILENCED_SYSTEM_CHECKS = [
    # W021: SECURE_HSTS_PRELOAD выключен намеренно — preload включается только
    # отдельным решением владельца (SPEC, разделы 11.3 и 15).
    "security.W021",
]
