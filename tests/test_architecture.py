"""Tests de la capa de servicios y del contenedor (listos para el backend)."""

from __future__ import annotations

import pytest

from app import create_app
from app.container import build
from app.models import AccountRequest, RegistrationError, RegistrationResult, RegistrationUnavailable
from app.repositories.disabled import DisabledAccountRepository
from app.services.accounts import AccountService
from app.services.status import StaticStatusService


class MemoryAccounts:
    """Repositorio en memoria: el mismo contrato que tendrá OpenMU."""

    def __init__(self, existing: set[str] | None = None) -> None:
        self.users = set(existing or ())

    def exists(self, username: str) -> bool:
        return username.lower() in self.users

    def create(self, request: AccountRequest) -> RegistrationResult:
        self.users.add(request.username.lower())
        return RegistrationResult(username=request.username)


def _req(**overrides) -> AccountRequest:
    data = {"username": "jugador1", "password": "secreto1", "password_confirm": "secreto1", "email": ""}
    data.update(overrides)
    return AccountRequest(**data)


def test_registration_disabled_raises():
    service = AccountService(MemoryAccounts(), enabled=False)
    with pytest.raises(RegistrationUnavailable):
        service.register(_req())


def test_registration_validates_fields():
    service = AccountService(MemoryAccounts(), enabled=True)
    with pytest.raises(RegistrationError) as err:
        service.register(_req(username="a b", password="123", password_confirm="123", email="nope"))
    assert set(err.value.field_errors) == {"username", "password", "email"}


def test_registration_checks_password_match_and_duplicates():
    service = AccountService(MemoryAccounts({"tomado"}), enabled=True)
    with pytest.raises(RegistrationError) as err:
        service.register(_req(password_confirm="otra123"))
    assert "password2" in err.value.field_errors
    with pytest.raises(RegistrationError) as err:
        service.register(_req(username="Tomado"))
    assert "username" in err.value.field_errors


def test_registration_creates_account():
    repo = MemoryAccounts()
    result = AccountService(repo, enabled=True).register(_req())
    assert result.username == "jugador1"
    assert repo.exists("JUGADOR1")


def test_account_request_hides_password():
    assert "secreto1" not in repr(_req())


def test_disabled_repository_never_creates():
    with pytest.raises(RegistrationUnavailable):
        DisabledAccountRepository().create(_req())


def test_static_status():
    assert StaticStatusService().current({"server": {"status_label": "Online"}}).online
    status = StaticStatusService().current({"server": {"status_label": "Mantenimiento"}})
    assert not status.online and status.source == "static"


def test_container_rejects_unknown_backend(app):
    config = dict(app.config, CONTENT_BACKEND="mongo")
    with pytest.raises(ValueError):
        build(config)


def test_container_db_backend_without_url_fails_fast(app):
    config = dict(app.config, CONTENT_BACKEND="db", DATABASE_URL="")
    with pytest.raises(ValueError):
        build(config)


def test_register_flow_with_backend(app):
    """Con el flag encendido y un repositorio que crea, el POST redirige."""
    app = create_app({"TESTING": True, "SECRET_KEY": "test", "WTF_CSRF_ENABLED": False, "FEATURE_REGISTRATION": True})
    repo = MemoryAccounts()
    app.extensions["muweb"].accounts = AccountService(repo, enabled=True)
    client = app.test_client()

    bad = client.post("/registro", data={"username": "x", "password": "1", "password2": "1"})
    assert bad.status_code == 422
    assert "4 a 10 letras" in bad.text

    ok = client.post(
        "/registro",
        data={"username": "jugador1", "password": "secreto1", "password2": "secreto1"},
    )
    assert ok.status_code == 302
    assert repo.exists("jugador1")
    assert "jugador1" in client.get(ok.headers["Location"]).text
