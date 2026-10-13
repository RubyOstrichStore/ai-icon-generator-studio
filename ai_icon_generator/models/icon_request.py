"""Typed request object passed between the UI and the orchestrator."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class IconRequest:
    prompt: str
    preset: str
    size: int = 512
    seed: int = 0
    backend: str = "sd-turbo-onnx"

    def validate(self) -> None:
        if not self.prompt.strip():
            raise ValueError("prompt required")
        if self.size not in (128, 256, 512, 1024):
            raise ValueError(f"unsupported size: {self.size}")