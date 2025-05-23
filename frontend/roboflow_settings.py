from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QGroupBox,
    QFormLayout, QLineEdit, QSpinBox, QPushButton,
    QMessageBox
)
from PyQt6.QtCore import pyqtSignal

class RoboflowSettingsDialog(QDialog):
    settings_updated = pyqtSignal()

    def __init__(self, db, parent=None):
        super().__init__(parent)
        self.db = db
        self.setWindowTitle("Roboflow Settings")
        self.setModal(True)
        self.setup_ui()
        self.load_settings()

    def setup_ui(self):
        self.setMinimumWidth(400)
        layout = QVBoxLayout(self)
        layout.setSpacing(12)
        layout.setContentsMargins(20, 20, 20, 20)

        roboflow_group = self._create_roboflow_group()
        layout.addWidget(roboflow_group)

        button_layout = self._create_button_layout()
        layout.addLayout(button_layout)
        self.setLayout(layout)

    def _create_roboflow_group(self):
        group = QGroupBox("Roboflow")
        layout = QFormLayout()
        layout.setSpacing(8)
        layout.setContentsMargins(15, 15, 15, 15)

        self.api_key = QLineEdit()
        self.api_key.setEchoMode(QLineEdit.EchoMode.Password)
        self.project = QLineEdit()
        self.version = QSpinBox()
        self.version.setMinimum(1)
        self.model_classes = QLineEdit()

        layout.addRow("API Key:", self.api_key)
        layout.addRow("Project:", self.project)
        layout.addRow("Version:", self.version)
        layout.addRow("Model Classes:", self.model_classes)

        group.setLayout(layout)
        return group

    def _create_button_layout(self):
        layout = QHBoxLayout()
        layout.setSpacing(10)

        save_btn = QPushButton("Save")
        save_btn.setMinimumWidth(100)
        save_btn.clicked.connect(self._save_settings)

        cancel_btn = QPushButton("Cancel")
        cancel_btn.setMinimumWidth(100)
        cancel_btn.clicked.connect(self.reject)

        layout.addStretch()
        layout.addWidget(save_btn)
        layout.addWidget(cancel_btn)

        return layout

    def load_settings(self):
        settings = self.db.get_roboflow_settings()
        if not settings:
            return

        self.api_key.setText(settings["api_key"])
        self.project.setText(settings["project"])
        self.version.setValue(int(settings["model_version"]))
        self.model_classes.setText(settings["model_classes"])

    def _save_settings(self):
        api_key = self.api_key.text().strip()
        project = self.project.text().strip()
        model_version = str(self.version.value())
        model_classes = self.model_classes.text().strip()

        if not all([api_key, project, model_classes]):
            QMessageBox.critical(self, "Error", "All fields are required")
            return

        success = self.db.update_roboflow_settings(
            api_key, project, model_version, model_classes
        )

        if success:
            self.settings_updated.emit()
            self.accept()
        else:
            QMessageBox.critical(self, "Error", "Failed to save settings")