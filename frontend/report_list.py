from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QHeaderView, QAbstractItemView, QMessageBox
from PyQt6.QtCore import Qt

class ReportList(QWidget):
    def __init__(self, db, parent=None):
        super().__init__(parent)
        self.db = db
        self.layout = QVBoxLayout(self)
        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels([
            "Block", "Subject", "Room", "Start", "End", "Date", "Students"
        ])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.table.cellDoubleClicked.connect(self._show_report_details)
        self.layout.addWidget(self.table)
        self.setLayout(self.layout)
        self.current_proctor_id = None

    def clear(self):
        self.current_proctor_id = None
        self.table.setRowCount(0)
        
    def display_reports(self, proctor_id):
        if not proctor_id or proctor_id < 0:
            self.clear()
            return
            
        self.current_proctor_id = proctor_id
        self.table.setRowCount(0)
        reports = self.db.get_reports_for_proctor(proctor_id)
        for row, report in enumerate(reports):
            self.table.insertRow(row)
            item_block = QTableWidgetItem(report["block"])
            item_block.setData(Qt.ItemDataRole.UserRole, report["id"])
            self.table.setItem(row, 0, item_block)
            self.table.setItem(row, 1, QTableWidgetItem(report["subject"]))
            self.table.setItem(row, 2, QTableWidgetItem(report["room"]))
            self.table.setItem(row, 3, QTableWidgetItem(str(report["start"])))
            self.table.setItem(row, 4, QTableWidgetItem(str(report["end"])))
            self.table.setItem(row, 5, QTableWidgetItem(str(report["date"])))
            self.table.setItem(row, 6, QTableWidgetItem(str(report["num_students"])))

    def _show_report_details(self, row, column):
        item = self.table.item(row, 0)
        report_id = item.data(Qt.ItemDataRole.UserRole)
        report = self.db.get_report(report_id)
        if not report:
            QMessageBox.critical(self, "Error", "Failed to load report details.")
            return
        details = (
            f"Report ID: {report['id']}\n"
            f"Block: {report['block']}\n"
            f"Subject: {report['subject']}\n"
            f"Room: {report['room']}\n"
            f"Start: {report['start']}\n"
            f"End: {report['end']}\n"
            f"Date: {report['date']}\n"
            f"Students: {report['num_students']}\n"
        )
        QMessageBox.information(self, "Report Details", details)
