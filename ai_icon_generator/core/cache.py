"""Content-addressed cache for prompt embeddings and rendered rasters.

Keyed by sha256(prompt + preset + size + seed + backend_id). Stored as
.npz under `.cache/`. Eviction is LRU by mtime with a configurable cap.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy as np

from ai_icon_generator.utils.logging_setup import get_logger

log = get_logger(__name__)


class RenderCache:
    def __init__(self, root: Path, max_entries: int = 512) -> None:
        self._root = root
        self._root.mkdir(parents=True, exist_ok=True)
        self._max = max_entries

    @staticmethod
    def key(*parts: object) -> str:
        payload = json.dumps(parts, sort_keys=True, default=str).encode()
        return hashlib.sha256(payload).hexdigest()[:32]

    def get(self, key: str) -> np.ndarray | None:
        path = self._root / f"{key}.npy"
        if not path.exists():
            return None
        try:
            return np.load(path)
        except (OSError, ValueError) as exc:
            log.warning("cache read failed for %s: %s", key, exc)
            return None

    def put(self, key: str, array: np.ndarray) -> None:
        np.save(self._root / f"{key}.npy", array)
        self._evict_if_needed()

    def _evict_if_needed(self) -> None:
        entries = sorted(self._root.glob("*.npy"), key=lambda p: p.stat().st_mtime)
        while len(entries) > self._max:
            victim = entries.pop(0)
            victim.unlink(missing_ok=True)