from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox

class ProctorEditorDialog(QDialog):
    def __init__(self, db, proctor_id=None, parent=None):
        super().__init__(parent)
        self.db = db
        self.proctor_id = proctor_id
        self.setWindowTitle("Edit Proctor" if proctor_id else "Add Proctor")
        self.setFixedSize(340, 220)
        layout = QVBoxLayout(self)
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Proctor Name")
        layout.addWidget(QLabel("Proctor Name:"))
        layout.addWidget(self.name_input)
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Email")
        layout.addWidget(QLabel("Email:"))
        layout.addWidget(self.email_input)
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(QLabel("Password:"))
        layout.addWidget(self.password_input)
        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self._handle_save)
        layout.addWidget(self.save_button)
        self.setLayout(layout)
        if proctor_id:
            self._load_proctor()

    def _load_proctor(self):
        proctor = self.db.get_proctor(self.proctor_id)
        if proctor:
            self.name_input.setText(proctor["proctor_name"])
            self.email_input.setText(proctor["email"])

    def _handle_save(self):
        name = self.name_input.text().strip()
        email = self.email_input.text().strip()
        password = self.password_input.text()
        if not name or not email or not password:
            QMessageBox.warning(self, "Error", "All fields are required.")
            return
        if self.proctor_id:
            success = self.db.update_proctor(self.proctor_id, name, email, password)
        else:
            success = self.db.add_proctor(name, email, password)
        if success:
            self.accept()
        else:
            QMessageBox.critical(self, "Error", "Failed to save proctor.")