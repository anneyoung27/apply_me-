from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QPushButton, QHBoxLayout
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon

from app.import_feature.CSVSettingWindow import CSVSettingsWindow
from app.import_feature.ImportToExcel import ExcelImporter

class ImporterWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Importer")
        self.setWindowIcon(QIcon("assets/others_icon/import.png"))
        self.setFixedSize(350, 220)
        self.setStyleSheet("""
            QDialog {
                background-color: #1e1e1e;
            }
            QLabel {
                color: #ffffff;
                font-size: 14px;
            }
            QPushButton {
                background-color: #2d2d2d;
                border: 1px solid #444;
                border-radius: 6px;
                padding: 10px;
                font-size: 13px;
                color: #fff;
            }
            QPushButton:hover {
                background-color: #3a3a3a;
            }
        """)

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignTop)

        # --- Header ---
        title = QLabel("Job Importer")
        title.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(title)

        subtitle = QLabel("To get started, please choose the import format")
        subtitle.setStyleSheet("font-size: 12px; color: #bbbbbb; margin-top: 6px;")
        layout.addWidget(subtitle)

        # --- Buttons Row ---
        btn_layout = QHBoxLayout()

        self.csv_btn = QPushButton("CSV")
        self.csv_btn.setIcon(QIcon("assets/head_menu/csv-file.png"))

        self.excel_btn = QPushButton("Excel")
        self.excel_btn.setIcon(QIcon("assets/head_menu/xlsx-file.png"))

        self.json_btn = QPushButton("JSON")
        self.json_btn.setIcon(QIcon("assets/head_menu/json-file.png"))

        btn_layout.addWidget(self.csv_btn)
        btn_layout.addWidget(self.excel_btn)
        btn_layout.addWidget(self.json_btn)

        layout.addSpacing(20)
        layout.addLayout(btn_layout)

    # === Import - likely JIRA XRAY ===
    def open_importer_window(self):
        win = ImporterWindow(self)

        win.csv_btn.clicked.connect(lambda: CSVSettingsWindow(self).exec())
        win.excel_btn.clicked.connect(lambda: ExcelImporter(self).import_from_excel())
        # win.json_btn.clicked.connect(lambda: JSONSettingsWindow(self).exec())

        win.exec()