"""Registro de cuentas.

Las reglas de validación viven acá y no en el controlador ni en la plantilla,
así el backend de OpenMU (v1) recibe siempre datos ya validados.
Antes de habilitarlo, confirmar las reglas contra la base real (docs/v1-db.md §5).
"""

from __future__ import annotations

import re

from ..models import AccountRequest, RegistrationError, RegistrationResult, RegistrationUnavailable
from ..repositories.base import AccountRepository

USERNAME_RE = re.compile(r"^[A-Za-z0-9]{4,10}$")
EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
PASSWORD_MIN = 6
PASSWORD_MAX = 10  # el cliente clásico no acepta más de 10


class AccountService:
    def __init__(self, repository: AccountRepository, *, enabled: bool) -> None:
        self.repository = repository
        self.enabled = enabled

    def validate(self, request: AccountRequest) -> dict[str, str]:
        """Errores por campo; vacío si todo está bien."""
        errors: dict[str, str] = {}
        if not USERNAME_RE.match(request.username):
            errors["username"] = "Usá de 4 a 10 letras o números, sin espacios."
        if not PASSWORD_MIN <= len(request.password) <= PASSWORD_MAX:
            errors["password"] = f"La contraseña tiene que tener entre {PASSWORD_MIN} y {PASSWORD_MAX} caracteres."
        elif request.password != request.password_confirm:
            errors["password2"] = "Las contraseñas no coinciden."
        if request.email and not EMAIL_RE.match(request.email):
            errors["email"] = "El email no parece válido."
        return errors

    def register(self, request: AccountRequest) -> RegistrationResult:
        """Valida y crea la cuenta.

        Lanza RegistrationUnavailable si el registro está apagado, o
        RegistrationError con los errores por campo.
        """
        if not self.enabled:
            raise RegistrationUnavailable("El registro por web todavía no está disponible.")
        errors = self.validate(request)
        if not errors and self.repository.exists(request.username):
            errors["username"] = "Ese usuario ya existe."
        if errors:
            raise RegistrationError(field_errors=errors)
        return self.repository.create(request)
