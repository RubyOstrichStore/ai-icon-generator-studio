"""Bootstrap: build the Qt app, load config, wire the orchestrator."""

from __future__ import annotations

import sys
from dataclasses import dataclass
from pathlib import Path

from PySide6.QtWidgets import QApplication

from ai_icon_generator.app.main_window import MainWindow
from ai_icon_generator.core.orchestrator import Orchestrator
from ai_icon_generator.services.model_registry import ModelRegistry
from ai_icon_generator.utils.config_loader import load_config


@dataclass(slots=True)
class BootstrapResult:
    app: QApplication
    window: MainWindow


def bootstrap(argv: list[str]) -> BootstrapResult:
    config = load_config(Path("config/studio.yaml"))
    registry = ModelRegistry.from_config(config.models)
    orchestrator = Orchestrator(registry=registry, config=config)

    app = QApplication(argv)
    app.setApplicationName("ai-icon-generator-studio")
    app.setOrganizationName("Tater Labs")

    window = MainWindow(orchestrator=orchestrator, config=config)
    return BootstrapResult(app=app, window=window)