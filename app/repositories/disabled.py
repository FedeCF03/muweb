"""Repositorio de cuentas para cuando no hay backend (v0)."""

from __future__ import annotations

from ..models import AccountRequest, RegistrationResult, RegistrationUnavailable


class DisabledAccountRepository:
    """No crea cuentas: el registro web queda apagado hasta la v1."""

    def exists(self, username: str) -> bool:
        return False

    def create(self, request: AccountRequest) -> RegistrationResult:
        raise RegistrationUnavailable("El registro por web todavía no está disponible.")
