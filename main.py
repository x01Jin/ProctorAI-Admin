from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QHBoxLayout, QSplitter
from PyQt6.QtCore import Qt
from frontend.toolbar import Toolbar
from frontend.proctor_list import ProctorList
from frontend.proctor_profile import ProctorProfile
from frontend.report_list import ReportList
from backend.auth import AdminLoginDialog
from backend.db import Database
from themes.theme import apply_fusion_dark_theme
import sys
import logs

class AdminMainWindow(QMainWindow):
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.setWindowTitle("ProctorAI Administrator Interface")
        self.setMinimumSize(1280, 720)
        self.toolbar = Toolbar(self)
        self.setMenuWidget(self.toolbar)
        self._init_ui()
        self.toolbar.refresh_requested.connect(self._refresh_all)

    def _init_ui(self):
        self.main_widget = QWidget()
        self.main_layout = QHBoxLayout(self.main_widget)
        self.splitter = QSplitter()
        self.proctor_list = ProctorList(self.db, self)
        self.profile_panel = QWidget()
        self.profile_layout = QSplitter()
        self.proctor_profile = ProctorProfile(self.db, self)
        self.report_list = ReportList(self.db, self)
        
        self.profile_layout.setOrientation(Qt.Orientation.Vertical)
        self.profile_layout.addWidget(self.proctor_profile)
        self.profile_layout.addWidget(self.report_list)
        
        self.profile_panel.setLayout(QHBoxLayout())
        self.profile_panel.layout().addWidget(self.profile_layout)
        
        self.splitter.addWidget(self.proctor_list)
        self.splitter.addWidget(self.profile_panel)
        self.splitter.setSizes([300, 900])
        
        self.main_layout.addWidget(self.splitter)
        self.setCentralWidget(self.main_widget)
        
        self.proctor_list.proctor_selected.connect(self._on_proctor_selected)
        self.toolbar.add_proctor_requested.connect(self.proctor_list.open_add_dialog)
        
        current_item = self.proctor_list.currentItem()
        if current_item:
            proctor_id = current_item.data(Qt.ItemDataRole.UserRole)
            self._on_proctor_selected(proctor_id)

    def _refresh_all(self):
        self.proctor_list.refresh()
        current_item = self.proctor_list.currentItem()
        if current_item:
            proctor_id = current_item.data(Qt.ItemDataRole.UserRole)
            self._on_proctor_selected(proctor_id)
        
    def _on_proctor_selected(self, proctor_id):
        self.proctor_profile.display_proctor(proctor_id)
        self.report_list.display_reports(proctor_id)


def main():
    logs.setup_logger()
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