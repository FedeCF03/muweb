"""Conexión a Postgres con un pool chico (psycopg 3)."""

from __future__ import annotations

from contextlib import contextmanager
from typing import Any, Iterator


class Database:
    """Envuelve un pool de conexiones. Se crea una vez por URL."""

    def __init__(self, url: str, *, min_size: int = 1, max_size: int = 5) -> None:
        if not url:
            raise ValueError("Falta la URL de la base (DATABASE_URL / OPENMU_DATABASE_URL)")
        # Acepta también el formato de SQLAlchemy (postgresql+psycopg://...)
        self.url = url.replace("postgresql+psycopg://", "postgresql://", 1)
        self.min_size = min_size
        self.max_size = max_size
        self._pool: Any = None

    def _get_pool(self) -> Any:
        if self._pool is None:
            try:
                from psycopg.rows import dict_row
                from psycopg_pool import ConnectionPool
            except ImportError as exc:  # pragma: no cover - depende del entorno
                raise RuntimeError(
                    "El backend Postgres necesita psycopg: pip install -r requirements-db.txt"
                ) from exc
            self._pool = ConnectionPool(
                self.url,
                min_size=self.min_size,
                max_size=self.max_size,
                kwargs={"row_factory": dict_row},
                open=True,
            )
        return self._pool

    @contextmanager
    def connection(self) -> Iterator[Any]:
        with self._get_pool().connection() as conn:
            yield conn

    def fetch_all(self, sql: str, params: tuple | dict | None = None) -> list[dict[str, Any]]:
        with self.connection() as conn:
            return list(conn.execute(sql, params).fetchall())

    def fetch_one(self, sql: str, params: tuple | dict | None = None) -> dict[str, Any] | None:
        with self.connection() as conn:
            return conn.execute(sql, params).fetchone()

    def close(self) -> None:
        if self._pool is not None:
            self._pool.close()
            self._pool = None
