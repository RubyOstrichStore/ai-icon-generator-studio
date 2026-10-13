"""Stage 4: export the raster as a multi-format icon set."""

from __future__ import annotations

from ai_icon_generator.core.orchestrator import PipelineContext
from ai_icon_generator.core.pipeline import export_icon_set
from ai_icon_generator.handlers import HandlerResult, register_handler
from ai_icon_generator.utils.naming import slugify


@register_handler("40_export")
def export_stage(ctx: PipelineContext) -> HandlerResult:
    raster = ctx.scratch.get("raster")
    if raster is None:
        return HandlerResult(ok=False, message="no raster", fatal=True)

    name = slugify(ctx.scratch["compiled"].text) or "icon"
    written = export_icon_set(raster, ctx.config.output_dir, name)
    ctx.outputs.extend(str(p) for p in written)
    return HandlerResult(ok=True, message=f"wrote {len(written)} file(s)")