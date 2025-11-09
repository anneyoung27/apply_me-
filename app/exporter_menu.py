import pandas as pd
from PySide6.QtWidgets import QFileDialog, QMessageBox

from app.models import Application


class DataExporter:
    def __init__(self, session, model):
        self.session = session
        self.model = Application

    def export_to_csv(self, parent=None):
        try:
            file_path, _ = QFileDialog.getSaveFileName(
                parent,
                "Save as CSV",
                "",
                "CSV Files (*.csv)"
            )
            if not file_path:
                return

            data = self._get_data()
            df = pd.DataFrame(data)
            df.to_csv(file_path, index=False, encoding='utf-8-sig')

            QMessageBox.information(parent, "Success", f"Data successfully exported to:\n{file_path}")
        except Exception as e:
            QMessageBox.critical(parent, "Error", f"Failed to export CSV:\n{e}")

    def export_to_excel(self, parent=None):
        try:
            file_path, _ = QFileDialog.getSaveFileName(
                parent,
                "Save as Excel",
                "",
                "Excel Files (*.xlsx)"
            )
            if not file_path:
                return

            data = self._get_data()
            df = pd.DataFrame(data)
            df.to_excel(file_path, index=False, engine="openpyxl")

            QMessageBox.information(parent, "Success", f"Data successfully exported to:\n{file_path}")
        except Exception as e:
            QMessageBox.critical(parent, "Error", f"Failed to export Excel:\n{e}")

    def _get_data(self):
        """Ambil semua data dari tabel terkait"""
        results = self.session.query(self.model).all()
        data = []
        for app in results:
            data.append({
                "ID": app.id,
                "Company": app.company_name,
                "Position": app.position,
                "Location": app.location,
                "Date Applied": app.date_applied.strftime("%d-%m-%Y") if app.date_applied else "",
                "Source": app.source,
                "Status": app.status,
                "Salary": app.salary_expectation,
                "Notes": app.notes,
            })
        return data
