"""Backend de archivos (v0): YAML y Markdown dentro de ``content/``."""

from .repositories import (
    FileClassRepository,
    FileDownloadRepository,
    FileEventRepository,
    FileFaqRepository,
    FileGalleryRepository,
    FileGameplayRepository,
    FileNewsRepository,
    FilePageRepository,
    FileSiteRepository,
)

__all__ = [
    "FileClassRepository",
    "FileDownloadRepository",
    "FileEventRepository",
    "FileFaqRepository",
    "FileGalleryRepository",
    "FileGameplayRepository",
    "FileNewsRepository",
    "FilePageRepository",
    "FileSiteRepository",
]
