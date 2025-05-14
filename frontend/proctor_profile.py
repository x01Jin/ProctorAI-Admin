from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt

class ProctorProfile(QWidget):
    def __init__(self, db, parent=None):
        super().__init__(parent)
        self.db = db
        self.layout = QVBoxLayout(self)
        self.name_label = QLabel()
        self.name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.name_label.setStyleSheet("font-size: 28px; font-weight: bold;")
        self.email_label = QLabel()
        self.email_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.email_label.setStyleSheet("font-size: 14px;")
        self.layout.addWidget(self.name_label)
        self.layout.addWidget(self.email_label)
        self.setLayout(self.layout)

    def display_proctor(self, proctor_id):
        proctor = self.db.get_proctor(proctor_id)
        if proctor:
            self.name_label.setText(proctor["proctor_name"])
            self.email_label.setText(proctor["email"])
        else:
            self.clear()
            
    def clear(self):
        self.name_label.setText("")
        self.email_label.setText("")