"""Model registry: resolves a backend id to a live backend instance.

Models are declared in `config/models.yaml` with a sha256 hash. The
registry verifies the hash on first load and caches the instance per
process.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from ai_icon_generator.services.diffusion_backend import (
    DiffusionBackend,
    OnnxDiffusionBackend,
    StubBackend,
)
from ai_icon_generator.utils.errors import ModelNotFoundError
from ai_icon_generator.utils.logging_setup import get_logger

log = get_logger(__name__)


@dataclass(slots=True)
class ModelSpec:
    id: str
    path: str
    sha256: str
    kind: str = "onnx"


@dataclass(slots=True)
class ModelRegistry:
    specs: dict[str, ModelSpec]
    _cache: dict[str, DiffusionBackend] = field(default_factory=dict)

    @classmethod
    def from_config(cls, specs: list[ModelSpec]) -> "ModelRegistry":
        return cls(specs={s.id: s for s in specs})

    def get(self, backend_id: str) -> DiffusionBackend:
        if backend_id in self._cache:
            return self._cache[backend_id]
        spec = self.specs.get(backend_id)
        if spec is None:
            raise ModelNotFoundError(f"unknown backend: {backend_id}")

        if spec.kind == "onnx":
            backend: DiffusionBackend = OnnxDiffusionBackend(spec)
        elif spec.kind == "stub":
            backend = StubBackend(spec)
        else:
            raise ModelNotFoundError(f"unsupported kind: {spec.kind}")

        self._cache[backend_id] = backend
        log.info("loaded backend %s (%s)", backend_id, spec.kind)
        return backend