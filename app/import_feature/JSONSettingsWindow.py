from PySide6.QtGui import QColor, QIcon
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QTextEdit, QPushButton,
    QHBoxLayout, QTableWidget, QTableWidgetItem, QMessageBox
)

from datetime import datetime
from app.database.Models import Application
import json


class JSONSettingsWindow(QDialog):
    def __init__(self, parent=None, session=None):
        super().__init__(parent)
        self.session = session
        self.setWindowTitle("JSON Import Settings")
        self.setWindowIcon(QIcon("assets/others_icon/json.png"))
        self.setMinimumWidth(600)

        layout = QVBoxLayout()

        # ===============================
        # Input JSON
        # ===============================
        layout.addWidget(QLabel("JSON:"))

        self.json_input = QTextEdit()

        self.json_input.setPlaceholderText("Paste your JSON here...")

        layout.addWidget(self.json_input)

        # Beautify button
        beautify_row = QHBoxLayout()
        self.beautify_btn = QPushButton("Beautify JSON")
        beautify_row.addWidget(self.beautify_btn)
        layout.addLayout(beautify_row)

        # ===============================
        # Preview Data (Table)
        # ===============================
        layout.addWidget(QLabel("Preview:"))

        self.table = QTableWidget()
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["Key", "Value"])
        self.table.horizontalHeader().setStretchLastSection(True)
        layout.addWidget(self.table)

        self.json_input.textChanged.connect(self.update_preview)
        self.beautify_btn.clicked.connect(self.beautify_json)

        # ===============================
        # Buttons
        # ===============================
        btn_row = QHBoxLayout()
        self.back_btn = QPushButton("Back")
        self.begin_btn = QPushButton("Begin Import")
        self.begin_btn.setStyleSheet("background-color: #1976d2; color: white;")

        btn_row.addWidget(self.back_btn)
        btn_row.addWidget(self.begin_btn)
        layout.addLayout(btn_row)

        self.back_btn.clicked.connect(self.close)
        self.begin_btn.clicked.connect(self.begin_import)
        self.back_btn.clicked.connect(self.close)

        self.setLayout(layout)

    # =============================
    # PREVIEW JSON → TABLE FORMAT
    # =============================
    def update_preview(self):
        text = self.json_input.toPlainText().strip()

        if not text:
            self.table.setRowCount(0)
            return

        try:
            data = json.loads(text)

            if not isinstance(data, dict):
                raise ValueError("JSON must be an object")

            self.table.setRowCount(len(data))

            for row, (k, v) in enumerate(data.items()):
                key_item = QTableWidgetItem(str(k))
                value_item = QTableWidgetItem(str(v))

                # --- warna sesuai permintaan ---
                key_item.setForeground(QColor("green"))
                value_item.setForeground(QColor("white"))

                self.table.setItem(row, 0, key_item)
                self.table.setItem(row, 1, value_item)

        except Exception:
            self.table.setRowCount(0)

    # ==============
    # BEAUTIFY JSON
    # ==============
    def beautify_json(self):
        text = self.json_input.toPlainText().strip()

        try:
            parsed = json.loads(text)
            pretty = json.dumps(parsed, indent=4)
            self.json_input.setPlainText(pretty)
        except Exception:
            QMessageBox.warning(self, "Invalid JSON", "Cannot beautify invalid JSON")

    def begin_import(self):

        # Ambil data dari preview table, bukan JSON langsung
        data = {}

        for row in range(self.table.rowCount()):
            key_item = self.table.item(row, 0)
            value_item = self.table.item(row, 1)

            if key_item and value_item:
                data[key_item.text()] = value_item.text()

        # Mandatory check
        mandatory = [
            "company_name", "position", "location", "date_applied",
            "source", "status", "salary_expectation", "notes"
        ]

        missing = [m for m in mandatory if not data.get(m)]
        if missing:
            QMessageBox.warning(self, "Missing Fields",
                                f"Missing mandatory fields: {', '.join(missing)}")
            return

        # --- ID generator ---
        company = data["company_name"].strip()
        prefix = company[:2].upper()

        last_app = (
            self.session.query(Application)
            .filter(Application.id.like(f"{prefix}%"))
            .order_by(Application.id.desc())
            .first()
        )

        if last_app:
            last_num = int(last_app.id[-3:])
            new_num = last_num + 1
        else:
            new_num = 1

        new_id = f"{prefix}{new_num:03d}"

        # --- Create application ---
        app = Application(
            id=new_id,
            company_name=data["company_name"],
            position=data["position"],
            location=data["location"],
            date_applied=datetime.strptime(data["date_applied"], "%Y-%m-%d").date(),
            source=data["source"],
            status=data["status"],
            salary_expectation=data["salary_expectation"],
            notes=data["notes"],
            created_at=datetime.now(),
        )

        self.session.add(app)
        self.session.commit()

        QMessageBox.information(self, "Imported", "JSON data imported successfully!")
        self.accept()