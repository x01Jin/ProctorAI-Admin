from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt6.QtCore import Qt
import hashlib

class AdminLoginDialog(QDialog):
    def __init__(self, db, parent=None):
        super().__init__(parent)
        self.db = db
        self.setWindowTitle("Admin Login")
        self.setFixedSize(320, 180)
        layout = QVBoxLayout(self)
        self.info_label = QLabel("Administrator Login")
        self.info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.info_label)
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Admin Username")
        layout.addWidget(self.username_input)
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.password_input)
        self.login_button = QPushButton("Login")
        self.login_button.clicked.connect(self._handle_login)
        layout.addWidget(self.login_button)
        self.setLayout(layout)

    def _handle_login(self):
        username = self.username_input.text().strip()
        password = self.password_input.text()
        if not username or not password:
            QMessageBox.warning(self, "Login Failed", "Please enter both username and password.")
            return
        admins = self.db.get_admin()
        if not admins:
            QMessageBox.critical(self, "Login Failed", "Admin account not found in database.")
            return
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        for admin in admins:
            if admin.get("user_role") == "admin" and \
               (username == admin["proctor_name"] or username == admin["email"]) and \
               admin["password"] == password_hash:
                self.accept()
                return
        QMessageBox.warning(self, "Login Failed", "Invalid username or password.")
