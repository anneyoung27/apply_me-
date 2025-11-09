import pandas as pd
from PySide6.QtWidgets import QFileDialog, QMessageBox
from app.database import SessionLocal
from app.models import Application


class DataImporter:
    def __init__(self, parent=None):
        self.parent = parent
        self.session = SessionLocal()

    def import_from_excel(self):
        try:
            # === Pilih file Excel ===
            file_path, _ = QFileDialog.getOpenFileName(
                self.parent,
                "Import Excel File",
                "",
                "Excel Files (*.xlsx)"
            )
            if not file_path:
                return

            # === Baca file Excel ===
            try:
                df = pd.read_excel(file_path, engine="openpyxl")
            except Exception as e:
                QMessageBox.critical(self.parent, "Read Error", f"Failed to read Excel file:\n{e}")
                return

            # === Cek jika kosong ===
            if df.empty:
                QMessageBox.warning(self.parent, "Empty File", "The selected Excel file is empty.")
                return

            # === Validasi kolom wajib ===
            required_columns = {"company_name", "position", "location", "date_applied", "status"}
            if not required_columns.issubset(df.columns):
                QMessageBox.critical(
                    self.parent,
                    "Invalid Format",
                    f"Excel file must contain these columns:\n{', '.join(required_columns)}"
                )
                return

            # === Import data ===
            count = 0
            for _, row in df.iterrows():
                app = Application(
                    company_name=str(row.get("company_name", "")).strip(),
                    position=str(row.get("position", "")).strip(),
                    location=str(row.get("location", "")).strip(),
                    date_applied=row.get("date_applied"),
                    source=str(row.get("source", "")).strip(),
                    status=str(row.get("status", "Applied")).strip(),
                    salary_expectation=str(row.get("salary_expectation", "")).strip(),
                    notes=str(row.get("notes", "")).strip(),
                )
                self.session.add(app)
                count += 1

            self.session.commit()

            QMessageBox.information(
                self.parent,
                "Import Success",
                f"Successfully imported {count} records from Excel file."
            )

        except Exception as e:
            QMessageBox.critical(
                self.parent,
                "Import Error",
                f"Failed to import Excel:\n{e}"
            )