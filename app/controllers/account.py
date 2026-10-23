"""Registro de cuentas.

El formulario siempre se muestra. Mientras FEATURE_REGISTRATION=0 queda
deshabilitado y el POST responde 503; con el flag y OpenMU configurado, el
servicio valida y el repositorio crea la cuenta.
"""

from __future__ import annotations

from flask import Blueprint, current_app, redirect, render_template, request, url_for

from ..container import services
from ..models import AccountRequest, RegistrationError, RegistrationUnavailable

bp = Blueprint("account", __name__, url_prefix="/registro")


def _form(**context):
    return render_template(
        "register.html",
        title="Crear cuenta",
        enabled=services().accounts.enabled,
        **context,
    )


@bp.get("")
def register():
    return _form(created=request.args.get("ok"))


@bp.post("")
def register_post():
    form = request.form
    account = AccountRequest(
        username=form.get("username", "").strip(),
        password=form.get("password", ""),
        password_confirm=form.get("password2", ""),
        email=form.get("email", "").strip(),
        ip=request.remote_addr,
    )
    values = {"username": account.username, "email": account.email}
    try:
        result = services().accounts.register(account)
    except RegistrationUnavailable as exc:
        return _form(error=str(exc), values=values), 503
    except RegistrationError as exc:
        return _form(error=exc.message, field_errors=exc.field_errors, values=values), 422
    current_app.logger.info("Cuenta creada desde la web: %s", result.username)
    return redirect(url_for("account.register", ok=result.username))
