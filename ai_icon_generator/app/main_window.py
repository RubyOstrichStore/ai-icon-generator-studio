"""Main window shell. Thin — all real work lives in handlers."""

from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QComboBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from ai_icon_generator.core.orchestrator import Orchestrator
from ai_icon_generator.utils.config_loader import StudioConfig


class MainWindow(QWidget):
    def __init__(self, orchestrator: Orchestrator, config: StudioConfig) -> None:
        super().__init__()
        self._orchestrator = orchestrator
        self._config = config

        self.setWindowTitle("AI Icon Generator Studio")
        self.resize(980, 640)

        self._prompt = QLineEdit(placeholderText="describe the icon…")
        self._preset = QComboBox()
        self._preset.addItems(config.presets)
        self._generate = QPushButton("Generate")
        self._generate.clicked.connect(self._on_generate)
        self._status = QLabel("ready")

        row = QHBoxLayout()
        row.addWidget(self._prompt, stretch=1)
        row.addWidget(self._preset)
        row.addWidget(self._generate)

        layout = QVBoxLayout(self)
        layout.addLayout(row)
        layout.addStretch(1)
        layout.addWidget(self._status, alignment=Qt.AlignLeft)

    def _on_generate(self) -> None:
        prompt = self._prompt.text().strip()
        if not prompt:
            self._status.setText("prompt is empty")
            return
        preset = self._preset.currentText()
        self._status.setText(f"generating… ({preset})")
        result = self._orchestrator.run(prompt=prompt, preset=preset)
        self._status.setText(result.summary)