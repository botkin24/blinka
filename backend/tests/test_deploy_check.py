import os
import subprocess
import sys
from pathlib import Path

from django.core.management.utils import get_random_secret_key

BACKEND_DIR = Path(__file__).resolve().parent.parent


def test_check_deploy_with_prod_settings_has_no_warnings():
    # Тестовые значения генерируются на лету; реальные секреты не используются.
    env = {
        **os.environ,
        "DJANGO_SETTINGS_MODULE": "config.settings.prod",
        "DJANGO_SECRET_KEY": get_random_secret_key(),
        "ADMIN_URL": "deploy-check-path/",
    }
    result = subprocess.run(
        [sys.executable, "manage.py", "check", "--deploy", "--fail-level", "WARNING"],
        cwd=BACKEND_DIR,
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )
    output = result.stdout + result.stderr
    assert result.returncode == 0, output
    assert "WARNINGS" not in output
