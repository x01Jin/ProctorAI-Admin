from PyQt6.QtWidgets import QToolBar
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtGui import QAction

class Toolbar(QToolBar):
    add_proctor_requested = pyqtSignal()
    refresh_requested = pyqtSignal()
    settings_requested = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_actions()

    def _setup_actions(self):
        add_proctor_action = QAction("Add Proctor", self)
        add_proctor_action.triggered.connect(self._on_add_proctor)
        self.addAction(add_proctor_action)

        refresh_action = QAction("Refresh", self)
        refresh_action.triggered.connect(self._on_refresh)
        self.addAction(refresh_action)

        settings_action = QAction("Settings", self)
        settings_action.triggered.connect(self._on_settings)
        self.addAction(settings_action)

    def _on_add_proctor(self):
        self.add_proctor_requested.emit()

    def _on_refresh(self):
        self.refresh_requested.emit()

    def _on_settings(self):
        self.settings_requested.emit()