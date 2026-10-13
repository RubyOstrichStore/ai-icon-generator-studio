"""Stage 1: compile the raw prompt against the active preset."""

from __future__ import annotations

from ai_icon_generator.core.orchestrator import PipelineContext
from ai_icon_generator.core.prompt_compiler import compile_prompt
from ai_icon_generator.handlers import HandlerResult, register_handler
from ai_icon_generator.services.preset_store import load_preset
from ai_icon_generator.utils.errors import PromptSyntaxError


@register_handler("10_compile")
def compile_stage(ctx: PipelineContext) -> HandlerResult:
    preset = load_preset(ctx.preset, ctx.config.preset_dir)
    try:
        compiled = compile_prompt(ctx.prompt, preset.tags)
    except PromptSyntaxError as exc:
        return HandlerResult(ok=False, message=str(exc), fatal=True)
    ctx.scratch["compiled"] = compiled
    return HandlerResult(ok=True)