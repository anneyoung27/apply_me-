from PySide6.QtCore import Qt, QTimer
from PySide6.QtWidgets import QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QComboBox, QHBoxLayout, QPushButton, \
    QMessageBox, QDialog, QProgressDialog
from datetime import datetime

from app.database.Database import SessionLocal
from app.database.Models import Application


class CSVFieldMappingWindow(QDialog):
    def __init__(self, parent, csv_path):
        super().__init__(parent)

        self.csv_path = csv_path
        self.setWindowTitle("Map fields")
        self.setMinimumWidth(600)

        layout = QVBoxLayout()

        header = QLabel("<h2>Map fields</h2>")
        desc = QLabel(
            "Select the CSV fields to import and how you would like these "
            "converted to fields in apply_me!"
        )
        desc.setWordWrap(True)

        layout.addWidget(header)
        layout.addWidget(desc)

        # ---- READ CSV HEADER ONLY ----
        import csv
        with open(csv_path, newline='', encoding="utf-8") as f:
            reader = csv.reader(f)
            headers = next(reader)
            headers = [h.replace("\ufeff", "").strip() for h in headers]  # remove BOM

        self.headers = headers

        # ---- MAPPING TABLE ----
        self.table = QTableWidget(len(headers), 2)
        self.table.setHorizontalHeaderLabels(["CSV Field", "apply_me Field"])

        db_fields = [
            "company_name", "position", "location", "date_applied",
            "source", "status", "salary_expectation", "notes"
        ]

        for row, h in enumerate(headers):
            item = QTableWidgetItem(h)
            item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            self.table.setItem(row, 0, item)

            combo = QComboBox()
            combo.addItems(db_fields)
            self.table.setCellWidget(row, 1, combo)

        layout.addWidget(self.table)

        # ---- BUTTONS ----
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()

        btn_back = QPushButton("Back")
        btn_begin = QPushButton("Begin Import")

        btn_back.clicked.connect(self.go_back)
        btn_begin.clicked.connect(self.begin_import)

        btn_layout.addWidget(btn_back)
        btn_layout.addWidget(btn_begin)

        layout.addLayout(btn_layout)
        self.setLayout(layout)

    # ==========================================================
    # BACK BUTTON — FIX FREEZE
    # ==========================================================
    def go_back(self):
        self.close()
        parent = self.parent()
        if parent and isinstance(parent, QDialog):
            parent.show()

    # ==========================================================
    # PARSE CSV WITH MAPPING (IMPORTANT!)
    # ==========================================================
    def parse_csv_using_mapping(self):
        import csv

        # ambil mapping CSV FIELD → DB FIELD
        mapping = {}
        for r in range(self.table.rowCount()):
            csv_field = self.table.item(r, 0).text().strip()
            db_field = self.table.cellWidget(r, 1).currentText().strip()
            mapping[csv_field] = db_field

        parsed = []

        # gunakan DictReader agar per kolom akurat
        with open(self.csv_path, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)

            for row in reader:
                new_row = {}
                for csv_key, val in row.items():
                    clean_key = csv_key.replace("\ufeff", "").strip()
                    db_field = mapping.get(clean_key)

                    if db_field:
                        # FIX di sini ↓↓↓
                        value = (val or "").strip()
                        new_row[db_field] = value

                parsed.append(new_row)

        return parsed

    # ==========================================================
    # BEGIN IMPORT — MAIN PROCESS
    # ==========================================================
    def begin_import(self):
        MANDATORY_FIELDS = [
            "company_name", "position", "location", "date_applied",
            "source", "status", "salary_expectation", "notes"
        ]

        imported_data = self.parse_csv_using_mapping()

        if not imported_data:
            QMessageBox.warning(self, "Error", "CSV contains no data.")
            return

        # ---- VALIDATION (per-row, tidak stop import) ----
        errors = []

        for idx, row in enumerate(imported_data, start=1):
            for f in MANDATORY_FIELDS:
                if f not in row or (row[f] or "").strip() == "":
                    errors.append(f"Row {idx}: Missing mandatory field '{f}'")

        # Tampilkan daftar error, tapi tidak stop import
        if errors:
            QMessageBox.warning(
                self,
                "Some rows contain missing fields",
                "The following issues were found:\n\n" + "\n".join(errors)
            )

        # ---- PROGRESS DIALOG ----
        progress = QProgressDialog("Importing data...", "Cancel", 0, len(imported_data), self)
        progress.setWindowModality(Qt.WindowModal)
        progress.setValue(0)

        self.import_data = imported_data
        self.import_index = 0

        def process_next():
            if progress.wasCanceled():
                return

            if self.import_index < len(imported_data):
                row = imported_data[self.import_index]

                # Skip row yang tidak valid
                missing = [f for f in MANDATORY_FIELDS if (row.get(f) or "").strip() == ""]
                if missing:
                    print(f"Skipping row {self.import_index + 1}, missing: {missing}")
                else:
                    generated_id = self.generate_id(row["company_name"])
                    self.insert_row_to_db(generated_id, row)

                self.import_index += 1
                progress.setValue(self.import_index)

                QTimer.singleShot(30, process_next)
            else:
                progress.close()
                QMessageBox.information(self, "Completed", "Import finished successfully!")

        QTimer.singleShot(100, process_next)

    # ==========================================================
    # GENERATE ID
    # ==========================================================
    def generate_id(self, company_name):
        prefix = company_name[:2].upper()

        session = SessionLocal()
        last_id = (
            session.query(Application.id)
            .filter(Application.id.like(f"{prefix}%"))
            .order_by(Application.id.desc())
            .first()
        )

        if last_id:
            last_seq = int(last_id[0][2:])
            new_seq = last_seq + 1
        else:
            new_seq = 1

        session.close()
        return f"{prefix}{new_seq:03d}"

    # ==========================================================
    # INSERT INTO DB
    # ==========================================================
    def insert_row_to_db(self, generated_id, row):
        session = SessionLocal()

        # PARSE DATE
        try:
            parsed_date = datetime.strptime(row["date_applied"], "%Y-%m-%d").date()
        except:
            parsed_date = None

        new_app = Application(
            id=generated_id,
            company_name=row["company_name"],
            position=row["position"],
            location=row["location"],
            date_applied=parsed_date,
            source=row["source"],
            status=row["status"],
            salary_expectation=row["salary_expectation"],
            notes=row["notes"],
            created_at=datetime.now()
        )

        session.add(new_app)
        session.commit()
        session.close()