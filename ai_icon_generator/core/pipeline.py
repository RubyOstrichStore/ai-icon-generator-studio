"""Low-level pipeline ops: prompt → latent → raster → icon set."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import numpy as np
from PIL import Image

from ai_icon_generator.services.diffusion_backend import DiffusionBackend


@dataclass(slots=True)
class Raster:
    pixels: np.ndarray  # HxWx4, uint8, RGBA
    size: int

    def to_pil(self) -> Image.Image:
        return Image.fromarray(self.pixels, mode="RGBA")


def render_raster(
    backend: DiffusionBackend,
    prompt_embedding: np.ndarray,
    size: int,
    seed: int,
) -> Raster:
    """Run the diffusion backend and return a single RGBA raster."""
    raw = backend.sample(embedding=prompt_embedding, size=size, seed=seed)
    if raw.shape != (size, size, 4):
        raise ValueError(f"backend returned {raw.shape}, expected {(size, size, 4)}")
    return Raster(pixels=raw, size=size)


def export_icon_set(raster: Raster, out_dir: Path, name: str) -> list[Path]:
    """Write PNG + ICO + ICNS variants. Returns list of written paths."""
    out_dir.mkdir(parents=True, exist_ok=True)
    img = raster.to_pil()

    written: list[Path] = []
    png_path = out_dir / f"{name}.png"
    img.save(png_path, format="PNG")
    written.append(png_path)

    ico_path = out_dir / f"{name}.ico"
    img.save(
        ico_path,
        format="ICO",
        sizes=[(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)],
    )
    written.append(ico_path)

    return written