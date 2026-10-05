import pytest
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

from config.settings.base import validate_admin_url


def test_standard_admin_path_returns_404(client):
    assert client.get("/admin/").status_code == 404
    assert client.get("/admin/login/").status_code == 404


def test_admin_login_opens_by_admin_url(client):
    response = client.get(f"/{settings.ADMIN_URL}login/")
    assert response.status_code == 200
    assert b'name="password"' in response.content


def test_admin_index_redirects_anonymous_to_login(client):
    response = client.get(f"/{settings.ADMIN_URL}")
    assert response.status_code == 302
    assert response.url.startswith(f"/{settings.ADMIN_URL}login/")


@pytest.mark.parametrize("value", ["admin/", "Admin/", "/secret/", "secret", "/", ""])
def test_invalid_admin_url_is_rejected(value):
    with pytest.raises(ImproperlyConfigured):
        validate_admin_url(value)
