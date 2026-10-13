"""Diffusion backend abstraction. ONNX runtime + a stub for tests."""

from __future__ import annotations

from typing import Protocol

import numpy as np

from ai_icon_generator.utils.logging_setup import get_logger

log = get_logger(__name__)


class DiffusionBackend(Protocol):
    def embed(self, text: str, tags: dict[str, str]) -> np.ndarray: ...
    def sample(self, embedding: np.ndarray, size: int, seed: int) -> np.ndarray: ...


class StubBackend:
    """Deterministic backend for tests and offline dev."""

    def __init__(self, spec) -> None:
        self._spec = spec

    def embed(self, text: str, tags: dict[str, str]) -> np.ndarray:
        seed = abs(hash((text, tuple(sorted(tags.items()))))) % (2**32)
        rng = np.random.default_rng(seed)
        return rng.standard_normal(512, dtype=np.float32)

    def sample(self, embedding: np.ndarray, size: int, seed: int) -> np.ndarray:
        rng = np.random.default_rng(seed)
        img = rng.integers(0, 256, size=(size, size, 4), dtype=np.uint8)
        img[..., 3] = 255
        return img


class OnnxDiffusionBackend:
    """Real backend. Lazily loads the ONNX session on first use."""

    def __init__(self, spec) -> None:
        self._spec = spec
        self._session = None

    def _ensure_session(self) -> None:
        if self._session is not None:
            return
        import onnxruntime as ort  # deferred — heavy import
        self._session = ort.InferenceSession(
            self._spec.path,
            providers=["CUDAExecutionProvider", "DmlExecutionProvider", "CPUExecutionProvider"],
        )

    def embed(self, text: str, tags: dict[str, str]) -> np.ndarray:
        self._ensure_session()
        tokens = np.frombuffer(text.encode("utf-8")[:512], dtype=np.uint8).astype(np.int64)
        out = self._session.run(None, {"tokens": tokens[None, :]})  # type: ignore[union-attr]
        return np.asarray(out[0], dtype=np.float32)

    def sample(self, embedding: np.ndarray, size: int, seed: int) -> np.ndarray:
        self._ensure_session()
        noise = np.random.default_rng(seed).standard_normal((1, 4, size // 8, size // 8), dtype=np.float32)
        out = self._session.run(  # type: ignore[union-attr]
            None,
            {"embedding": embedding[None, :], "noise": noise},
        )
        img = np.asarray(out[0])
        img = np.clip((img + 1.0) * 127.5, 0, 255).astype(np.uint8)
        return np.transpose(img, (1, 2, 0))