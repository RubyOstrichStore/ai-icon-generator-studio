"""Load `config/studio.yaml` into a typed StudioConfig."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import yaml

from ai_icon_generator.services.model_registry import ModelSpec


@dataclass(slots=True)
class StudioConfig:
    backend: str
    icon_size: int
    seed: int
    output_dir: Path
    cache_dir: Path
    preset_dir: Path
    presets: list[str]
    models: list[ModelSpec]


def load_config(path: Path) -> StudioConfig:
    blob = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    models = [
        ModelSpec(id=m["id"], path=m["path"], sha256=m["sha256"], kind=m.get("kind", "onnx"))
        for m in blob.get("models", [])
    ]
    return StudioConfig(
        backend=blob.get("backend", "sd-turbo-onnx"),
        icon_size=int(blob.get("icon_size", 512)),
        seed=int(blob.get("seed", 0)),
        output_dir=Path(blob.get("output_dir", "generated_icons")),
        cache_dir=Path(blob.get("cache_dir", ".cache")),
        preset_dir=Path(blob.get("preset_dir", "presets")),
        presets=list(blob.get("presets", [])),
        models=models,
    )