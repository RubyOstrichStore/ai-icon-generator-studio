"""Loads style presets from `presets/`. Plain YAML, safe_load only."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

import yaml

from ai_icon_generator.utils.errors import PresetNotFoundError


@dataclass(slots=True)
class StylePreset:
    name: str
    tags: dict[str, str] = field(default_factory=dict)
    negative: str = ""


def load_preset(name: str, preset_dir: Path) -> StylePreset:
    path = preset_dir / f"{name}.yaml"
    if not path.exists():
        raise PresetNotFoundError(f"preset not found: {name}")
    blob = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    return StylePreset(
        name=name,
        tags={str(k): str(v) for k, v in (blob.get("tags") or {}).items()},
        negative=str(blob.get("negative", "")),
    )


def list_presets(preset_dir: Path) -> list[str]:
    return sorted(p.stem for p in preset_dir.glob("*.yaml"))