"""Slugify prompts into filesystem-safe icon names."""

from __future__ import annotations

import re
import unicodedata

_NON_ALNUM = re.compile(r"[^a-z0-9]+")


def slugify(text: str, max_len: int = 48) -> str:
    norm = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode()
    slug = _NON_ALNUM.sub("-", norm.lower()).strip("-")
    return slug[:max_len].rstrip("-")