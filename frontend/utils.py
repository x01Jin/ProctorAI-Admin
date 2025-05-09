from PyQt6.QtWidgets import QInputDialog, QMessageBox

def confirm_proctor_deletion(parent, proctor_name):
    text, ok = QInputDialog.getText(
        parent,
        "Confirm Deletion",
        f"Type the proctor name '{proctor_name}' to confirm deletion:"
    )
    if ok and text.strip() == proctor_name:
        return True
    if ok:
        QMessageBox.warning(parent, "Incorrect", "Proctor name does not match.")
    return False