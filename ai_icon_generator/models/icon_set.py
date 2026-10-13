"""The result of a successful pipeline run."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(slots=True)
class IconSet:
    name: str
    files: list[Path]
    preset: str
    backend: str

    @property
    def primary(self) -> Path:
        return self.files[0]

    def summary(self) -> str:
        return f"{self.name} · {len(self.files)} file(s) · {self.preset} · {self.backend}"