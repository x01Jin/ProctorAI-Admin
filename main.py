from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QHBoxLayout, QSplitter
from frontend.toolbar import Toolbar
from frontend.proctor_list import ProctorList
from frontend.proctor_profile import ProctorProfile
from frontend.report_list import ReportList
from backend.auth import AdminLoginDialog
from backend.db import Database
from themes.theme import apply_fusion_dark_theme
import sys

class AdminMainWindow(QMainWindow):
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.setWindowTitle("ProctorAI Administrator Interface")
        self.setMinimumSize(1280, 720)
        self.toolbar = Toolbar(self)
        self.setMenuWidget(self.toolbar)
        self._init_ui()

    def _init_ui(self):
        main_widget = QWidget()
        main_layout = QHBoxLayout(main_widget)
        splitter = QSplitter()
        self.proctor_list = ProctorList(self.db, self)
        self.profile_panel = QWidget()
        profile_layout = QSplitter()
        self.proctor_profile = ProctorProfile(self.db, self)
        self.report_list = ReportList(self.db, self)
        from PyQt6.QtCore import Qt
        print(type(profile_layout), "setOrientation arg:", Qt.Orientation.Vertical)
        profile_layout.setOrientation(Qt.Orientation.Vertical)
        profile_layout.addWidget(self.proctor_profile)
        profile_layout.addWidget(self.report_list)
        self.profile_panel.setLayout(QHBoxLayout())
        self.profile_panel.layout().addWidget(profile_layout)
        splitter.addWidget(self.proctor_list)
        splitter.addWidget(self.profile_panel)
        splitter.setSizes([300, 900])
        main_layout.addWidget(splitter)
        self.setCentralWidget(main_widget)
        self.proctor_list.proctor_selected.connect(self._on_proctor_selected)
        self.toolbar.add_proctor_requested.connect(self.proctor_list.open_add_dialog)

    def _on_proctor_selected(self, proctor_id):
        self.proctor_profile.display_proctor(proctor_id)
        self.report_list.display_reports(proctor_id)

def main():
    app = QApplication(sys.argv)
    apply_fusion_dark_theme(app)
    db = Database()
    db.connect()
    login = AdminLoginDialog(db)
    if login.exec() != 1:
        sys.exit(0)
    window = AdminMainWindow(db)
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()