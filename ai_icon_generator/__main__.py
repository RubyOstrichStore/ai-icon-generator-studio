"""Bootstrap entry point for the desktop studio.

Launches the Qt application, wires the orchestrator, and hands control
to the main window. All heavy imports are deferred until after the
splash so cold start stays under ~700ms on a warm cache.
"""

from __future__ import annotations

import sys
from pathlib import Path

from ai_icon_generator.app.bootstrap import bootstrap
from ai_icon_generator.utils.logging_setup import configure_logging


def main() -> int:
    configure_logging(log_dir=Path("logs"))
    app, window = bootstrap(sys.argv)
    window.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())