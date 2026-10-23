"""Lectura de archivos con cache por mtime.

El cache se invalida solo: si cambia el mtime de un archivo (o de cualquier
archivo de un directorio), se vuelve a leer. Así el operador edita content/ y
recarga la página sin reiniciar nada.
"""

from __future__ import annotations

import re
from pathlib import Path
from threading import Lock
from typing import Any, Callable, TypeVar

import yaml

T = TypeVar("T")

_FRONT_MATTER = re.compile(r"^---\s*\n(.*?)\n---\s*\n?", re.S)


class FileStore:
    """Acceso a un directorio de contenido."""

    def __init__(self, root: Path) -> None:
        self.root = Path(root)
        self._cache: dict[str, tuple[float, Any]] = {}
        self._lock = Lock()

    def path(self, name: str) -> Path:
        return self.root / name

    def cached(self, key: Path, loader: Callable[[], T], *, stamp: float | None = None) -> T:
        """Cachea ``loader()`` hasta que cambie el mtime de ``key``."""
        current = stamp if stamp is not None else (key.stat().st_mtime if key.exists() else 0.0)
        with self._lock:
            hit = self._cache.get(str(key))
        if hit is not None and hit[0] == current:
            return hit[1]
        value = loader()
        with self._lock:
            self._cache[str(key)] = (current, value)
        return value

    def yaml(self, name: str) -> dict[str, Any]:
        """Un YAML del directorio como diccionario ({} si no existe)."""
        path = self.path(name)

        def load() -> dict[str, Any]:
            if not path.exists():
                return {}
            with path.open(encoding="utf-8") as fh:
                data = yaml.safe_load(fh) or {}
            if not isinstance(data, dict):
                raise ValueError(f"{path} debería contener un diccionario YAML")
            return data

        return self.cached(path, load)

    def text(self, name: str) -> str:
        path = self.path(name)
        return self.cached(path, lambda: path.read_text(encoding="utf-8") if path.exists() else "")

    def dir_stamp(self, directory: Path, pattern: str = "*") -> float:
        """Sello de un directorio: el mtime más reciente de sus archivos."""
        if not directory.exists():
            return 0.0
        stamps = [p.stat().st_mtime for p in directory.glob(pattern) if p.is_file()]
        return max(stamps) if stamps else 0.0


def split_front_matter(text: str) -> tuple[dict[str, Any], str]:
    """Separa el front matter (YAML entre --- ---) del cuerpo en Markdown."""
    match = _FRONT_MATTER.match(text)
    if not match:
        return {}, text
    meta = yaml.safe_load(match.group(1)) or {}
    return (meta if isinstance(meta, dict) else {}), text[match.end() :]
