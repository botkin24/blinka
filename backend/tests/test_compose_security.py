"""Статическая проверка docker-compose по SPEC 3 и 11.6 (без запуска Docker)."""

import re
from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[2]
SERVICES = {"db", "backend", "frontend", "caddy"}


def load(name: str) -> dict:
    return yaml.safe_load((ROOT / name).read_text(encoding="utf-8"))


@pytest.fixture(scope="module")
def compose() -> dict:
    return load("docker-compose.yml")


@pytest.fixture(scope="module")
def override() -> dict:
    return load("docker-compose.override.yml")


def test_all_services_present(compose):
    assert set(compose["services"]) == SERVICES


def test_only_caddy_publishes_80_and_443(compose):
    published = {name: svc.get("ports") for name, svc in compose["services"].items()}
    assert {name for name, ports in published.items() if ports} == {"caddy"}
    assert sorted(published["caddy"]) == ["443:443", "80:80"]


def test_override_binds_ports_only_to_localhost(override):
    for name, svc in (override.get("services") or {}).items():
        for port in svc.get("ports", []):
            assert str(port).startswith("127.0.0.1:"), f"{name}: {port}"


@pytest.mark.parametrize("service", sorted(SERVICES))
def test_service_hardening(compose, service):
    svc = compose["services"][service]
    assert "no-new-privileges:true" in svc["security_opt"]
    assert svc["cap_drop"] == ["ALL"]
    assert svc["deploy"]["resources"]["limits"]["memory"]
    for volume in svc.get("volumes", []):
        assert "docker.sock" not in volume


def test_only_caddy_gets_net_bind_service(compose):
    caps = {name: svc.get("cap_add") for name, svc in compose["services"].items()}
    assert caps == {"db": None, "backend": None, "frontend": None, "caddy": ["NET_BIND_SERVICE"]}


def test_images_pinned_to_exact_version(compose):
    images = [svc["image"] for svc in compose["services"].values() if "image" in svc]
    for dockerfile in ("backend/Dockerfile", "frontend/Dockerfile"):
        text = (ROOT / dockerfile).read_text(encoding="utf-8")
        images += re.findall(r"^FROM\s+(\S+)", text, flags=re.MULTILINE)
        images += re.findall(r"COPY --from=(\S+:\S+)", text)
    for image in images:
        # У Postgres точная версия — major.minor (16.15), у остальных — x.y.z.
        exact = r":\d+\.\d+(-|$)" if image.startswith("postgres:") else r":\d+\.\d+\.\d+"
        assert re.search(exact, image), image


def test_networks(compose):
    assert compose["networks"]["internal"]["internal"] is True
    networks = {name: set(svc["networks"]) for name, svc in compose["services"].items()}
    assert networks == {
        "db": {"internal"},
        "frontend": {"internal"},
        "backend": {"internal", "egress"},
        "caddy": {"internal", "edge"},
    }
