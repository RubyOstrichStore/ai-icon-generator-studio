"""Stage 3: run diffusion and produce a raster."""

from __future__ import annotations

from ai_icon_generator.core.orchestrator import PipelineContext
from ai_icon_generator.core.pipeline import render_raster
from ai_icon_generator.handlers import HandlerResult, register_handler


@register_handler("30_render")
def render_stage(ctx: PipelineContext) -> HandlerResult:
    embedding = ctx.scratch.get("embedding")
    if embedding is None:
        return HandlerResult(ok=False, message="no embedding", fatal=True)

    backend = ctx.registry.get(ctx.config.backend)
    raster = render_raster(
        backend=backend,
        prompt_embedding=embedding,
        size=ctx.config.icon_size,
        seed=ctx.config.seed,
    )
    ctx.scratch["raster"] = raster
    return HandlerResult(ok=True)