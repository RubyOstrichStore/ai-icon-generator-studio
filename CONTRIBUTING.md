# Contributing to ai-icon-generator-studio

Thanks for wanting to help build the tater of icon generators. This repo
is a layered Windows desktop utility written in Python that turns text
prompts, reference images, and style presets into production-ready icon
sets (ICO, PNG, SVG wrappers, and multi-resolution ICNS).

## Ground rules

- Python 3.11+ required. We target Windows 10/11 x64 as the primary
  platform, but the core engine runs cross-platform for CI.
- One feature per PR. If you're adding a new diffusion backend, that's
  one PR. If you're adding a new exporter, that's another.
- Every new handler under `handlers/` must register itself in
  `handlers/__init__.py` via the `@register_handler` decorator.
- No silent failures. Handlers return `HandlerResult` objects; the
  orchestrator logs every non-OK result.
- Tests go under `tests/`. If you touch the pipeline, add a test that
  proves the change.

## Development setup

```
git clone https://github.com/yourname/ai-icon-generator-studio
cd ai-icon-generator-studio
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python -m ai_icon_generator
```

## Style

- Black + isort + ruff. Pre-commit hooks live in `.pre-commit-config.yaml`
  (add them if you're the first contributor to care).
- Type hints required on public functions. `mypy --strict` on `core/`.
- Docstrings in Google style. Keep them short.

## Commit messages

`<scope>: <imperative summary>`

Examples:
- `handlers: add svg wrapper exporter`
- `core: fix cache key collision on duplicate prompts`
- `services: retry model download on 503`

## Reporting bugs

Open an issue with the OS build, Python version, backend (CPU/CUDA/DML),
and the exact prompt + preset that failed. Attach the log from
`logs/studio.log`.