"""Handler registry. Every stage registers itself here.

Handlers are pure functions over `PipelineContext`. They return a
`HandlerResult`. A fatal result aborts the pipeline.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Protocol

from ai_icon_generator.core.orchestrator import PipelineContext


@dataclass(slots=True)
class HandlerResult:
    ok: bool
    message: str = ""
    fatal: bool = False


class Handler(Protocol):
    def __call__(self, ctx: PipelineContext) -> HandlerResult: ...


HANDLERS: dict[str, Handler] = {}


def register_handler(name: str) -> Callable[[Handler], Handler]:
    def _wrap(fn: Handler) -> Handler:
        if name in HANDLERS:
            raise RuntimeError(f"handler already registered: {name}")
        HANDLERS[name] = fn
        return fn
    return _wrap


# Import side-effect: registers all built-in stages.
from ai_icon_generator.handlers import (  # noqa: E402,F401
    compile_stage,
    embed_stage,
    render_stage,
    export_stage,
)