"""Compile a raw prompt + preset into a normalized embedding input.

The studio supports three prompt dialects:
  - plain text ("a fox, flat, minimal")
  - slash directives ("/style=flat /palette=mono a fox")
  - JSON blobs ("{\"subject\":\"fox\",\"style\":\"flat\"}")

All three normalize to a `CompiledPrompt` with a canonical text and a
bag of tags the backend can consume.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field

from ai_icon_generator.utils.errors import PromptSyntaxError

_DIRECTIVE = re.compile(r"/(\w+)=([^\s]+)")


@dataclass(slots=True)
class CompiledPrompt:
    text: str
    tags: dict[str, str] = field(default_factory=dict)
    negative: str = ""


def compile_prompt(raw: str, preset_tags: dict[str, str]) -> CompiledPrompt:
    stripped = raw.strip()
    if not stripped:
        raise PromptSyntaxError("prompt is empty")

    if stripped.startswith("{"):
        return _compile_json(stripped, preset_tags)
    return _compile_text(stripped, preset_tags)


def _compile_json(raw: str, preset_tags: dict[str, str]) -> CompiledPrompt:
    try:
        blob = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise PromptSyntaxError(f"invalid JSON prompt: {exc.msg}") from exc
    text = str(blob.get("subject", "")).strip()
    tags = {**preset_tags, **{k: str(v) for k, v in blob.items() if k != "subject"}}
    negative = str(blob.get("negative", ""))
    return CompiledPrompt(text=text, tags=tags, negative=negative)


def _compile_text(raw: str, preset_tags: dict[str, str]) -> CompiledPrompt:
    tags = dict(preset_tags)
    text_parts: list[str] = []
    for token in raw.split():
        m = _DIRECTIVE.fullmatch(token)
        if m:
            tags[m.group(1)] = m.group(2)
        else:
            text_parts.append(token)
    return CompiledPrompt(text=" ".join(text_parts), tags=tags)