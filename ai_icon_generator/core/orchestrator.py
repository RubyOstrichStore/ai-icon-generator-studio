"""Orchestrator: routes a request through handlers in order.

Handlers register themselves via `register_handler`. The orchestrator
walks the registered stages, passes a shared `PipelineContext` down the
chain, and stops early if any stage returns a fatal error.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from ai_icon_generator.handlers import HANDLERS, HandlerResult
from ai_icon_generator.services.model_registry import ModelRegistry
from ai_icon_generator.utils.config_loader import StudioConfig
from ai_icon_generator.utils.logging_setup import get_logger

log = get_logger(__name__)


@dataclass(slots=True)
class PipelineContext:
    prompt: str
    preset: str
    config: StudioConfig
    registry: ModelRegistry
    scratch: dict[str, Any] = field(default_factory=dict)
    outputs: list[str] = field(default_factory=list)


@dataclass(slots=True)
class RunResult:
    ok: bool
    summary: str
    outputs: list[str]


class Orchestrator:
    def __init__(self, registry: ModelRegistry, config: StudioConfig) -> None:
        self._registry = registry
        self._config = config

    def run(self, prompt: str, preset: str) -> RunResult:
        ctx = PipelineContext(
            prompt=prompt,
            preset=preset,
            config=self._config,
            registry=self._registry,
        )
        for name, handler in HANDLERS.items():
            result: HandlerResult = handler(ctx)
            if not result.ok:
                log.warning("handler %s failed: %s", name, result.message)
                if result.fatal:
                    return RunResult(False, f"{name}: {result.message}", ctx.outputs)
        return RunResult(True, f"done — {len(ctx.outputs)} icon(s)", ctx.outputs)