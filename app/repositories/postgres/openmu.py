"""Cuentas en la base de OpenMU.

IMPORTANTE: antes de habilitar el registro hay que confirmar contra la base
real (docs/v1-db.md §5): nombre exacto de la tabla y columnas de "Account",
reglas del login y cómo hashea OpenMU la contraseña (algoritmo y costo).
Hasta entonces ``create`` se niega a escribir: mejor un registro apagado que
cuentas que no pueden entrar al juego.
"""

from __future__ import annotations

from ...models import AccountRequest, RegistrationResult, RegistrationUnavailable
from .connection import Database

# Ajustar a lo que muestre la base real (\d "Account" en psql).
ACCOUNT_TABLE = '"Account"'
LOGIN_COLUMN = '"LoginName"'


class OpenMuAccountRepository:
    def __init__(self, db: Database, *, writes_verified: bool = False) -> None:
        self.db = db
        # Se pone en True solo después de probar un INSERT y entrar al juego.
        self.writes_verified = writes_verified

    def exists(self, username: str) -> bool:
        row = self.db.fetch_one(
            f"SELECT 1 FROM {ACCOUNT_TABLE} WHERE lower({LOGIN_COLUMN}) = lower(%s) LIMIT 1",
            (username,),
        )
        return row is not None

    def create(self, request: AccountRequest) -> RegistrationResult:
        if not self.writes_verified:
            raise RegistrationUnavailable(
                "El registro todavía no está conectado a OpenMU. Pedí tu cuenta por Discord."
            )
        # TODO(v1): INSERT en "Account" con el hash que usa OpenMU, dentro de una
        # transacción, y registro en muweb.web_registration (sin la contraseña).
        raise NotImplementedError("Implementar el INSERT verificado contra OpenMU (docs/v1-db.md §5)")
