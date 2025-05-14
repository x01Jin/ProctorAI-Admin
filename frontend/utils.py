from PyQt6.QtWidgets import QInputDialog, QMessageBox

def confirm_proctor_deletion(parent, proctor_name, report_count=0):
    warning = (
        f"WARNING: This will permanently delete:\n\n"
        f"• Proctor: {proctor_name}\n"
        f"• Associated Reports: {report_count}\n\n"
        f"This action CANNOT be undone!\n\n"
        f"Type the proctor name '{proctor_name}' to confirm this destructive action:"
    )
    
    text, ok = QInputDialog.getText(
        parent,
        "⚠️ Confirm Destructive Action",
        warning
    )
    if ok and text.strip() == proctor_name:
        return True
    if ok:
        QMessageBox.warning(parent, "Incorrect", "Proctor name does not match.")
    return False