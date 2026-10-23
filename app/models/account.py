"""Modelos del registro de cuentas."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class AccountRequest:
    """Lo que manda el formulario de registro. La contraseña nunca se loguea."""

    username: str
    password: str
    password_confirm: str
    email: str = ""
    ip: str | None = None

    def __repr__(self) -> str:  # que la contraseña no aparezca en logs ni tracebacks
        return f"AccountRequest(username={self.username!r}, email={self.email!r}, ip={self.ip!r})"


@dataclass(frozen=True)
class RegistrationResult:
    """Resultado de un registro exitoso."""

    username: str


class RegistrationUnavailable(Exception):
    """El registro web no está habilitado (v0, o backend sin cuentas)."""


@dataclass
class RegistrationError(Exception):
    """Errores de validación, por campo. ``field_errors["username"] = "..."``."""

    field_errors: dict[str, str] = field(default_factory=dict)
    message: str = "Revisá los datos del formulario."

    def __str__(self) -> str:
        return self.message
