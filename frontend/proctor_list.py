from PyQt6.QtWidgets import QListWidget, QListWidgetItem, QMenu, QMessageBox
from PyQt6.QtCore import pyqtSignal, Qt

class ProctorList(QListWidget):
    proctor_selected = pyqtSignal(int)

    def __init__(self, db, parent=None):
        super().__init__(parent)
        self.db = db
        self.setMinimumWidth(300)
        self.setSelectionMode(self.SelectionMode.SingleSelection)
        self.itemClicked.connect(self._on_item_clicked)
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self._show_context_menu)
        self.refresh()

    def refresh(self):
        self.clear()
        proctors = self.db.get_proctors()
        for proctor in proctors:
            item = QListWidgetItem(proctor["proctor_name"])
            item.setData(Qt.ItemDataRole.UserRole, proctor["id"])
            self.addItem(item)

    def _on_item_clicked(self, item):
        proctor_id = item.data(Qt.ItemDataRole.UserRole)
        self.proctor_selected.emit(proctor_id)

    def _show_context_menu(self, pos):
        item = self.itemAt(pos)
        if not item:
            return
        proctor_id = item.data(Qt.ItemDataRole.UserRole)
        menu = QMenu(self)
        edit_action = menu.addAction("Edit Proctor")
        delete_action = menu.addAction("Delete Proctor")
        action = menu.exec(self.mapToGlobal(pos))
        if action == edit_action:
            self.open_edit_dialog(proctor_id)
        elif action == delete_action:
            self._confirm_delete(proctor_id, item.text())

    def open_add_dialog(self):
        from .proctor_editor import ProctorEditorDialog
        dialog = ProctorEditorDialog(self.db, parent=self)
        if dialog.exec() == 1:
            self.refresh()

    def open_edit_dialog(self, proctor_id):
        from .proctor_editor import ProctorEditorDialog
        dialog = ProctorEditorDialog(self.db, proctor_id=proctor_id, parent=self)
        if dialog.exec() == 1:
            self.refresh()

    def _confirm_delete(self, proctor_id, proctor_name):
        from .utils import confirm_proctor_deletion
        if confirm_proctor_deletion(self, proctor_name):
            if self.db.delete_proctor(proctor_id):
                self.refresh()
            else:
                QMessageBox.critical(self, "Error", "Failed to delete proctor.")