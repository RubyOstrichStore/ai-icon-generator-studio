"""Stage 2: turn the compiled prompt into a backend embedding."""

from __future__ import annotations

import numpy as np

from ai_icon_generator.core.cache import RenderCache
from ai_icon_generator.core.orchestrator import PipelineContext
from ai_icon_generator.handlers import HandlerResult, register_handler


@register_handler("20_embed")
def embed_stage(ctx: PipelineContext) -> HandlerResult:
    compiled = ctx.scratch.get("compiled")
    if compiled is None:
        return HandlerResult(ok=False, message="no compiled prompt", fatal=True)

    backend = ctx.registry.get(ctx.config.backend)
    cache = RenderCache(ctx.config.cache_dir)
    key = RenderCache.key("embed", ctx.config.backend, compiled.text, compiled.tags)

    cached = cache.get(key)
    if cached is not None:
        ctx.scratch["embedding"] = cached
        return HandlerResult(ok=True, message="embedding cache hit")

    embedding: np.ndarray = backend.embed(compiled.text, compiled.tags)
    cache.put(key, embedding)
    ctx.scratch["embedding"] = embedding
    return HandlerResult(ok=True)