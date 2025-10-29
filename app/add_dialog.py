from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QFormLayout,
    QLabel, QLineEdit, QDateEdit, QComboBox, QPushButton, QFrame
)
from PySide6.QtCore import Qt, QDate
from PySide6.QtGui import QFont, QColor


class AddDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("＋ Add Application")
        self.setFixedSize(420, 400)
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(15)

        # --- Header ---
        header = QLabel("Add New Application")
        header.setFont(QFont("Segoe UI", 18, QFont.Bold))
        header.setAlignment(Qt.AlignCenter)
        layout.addWidget(header, alignment=Qt.AlignHCenter)

        # Divider
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setStyleSheet("color: #ccc; margin-bottom: 10px;")
        layout.addWidget(line)

        # --- Error Message (hidden by default) ---
        self.error_label = QLabel("")
        self.error_label.setAlignment(Qt.AlignCenter)
        self.error_label.setStyleSheet("""
            QLabel {
                color: #C0392B;
                background-color: #FDEDEC;
                border: 1px solid #E6B0AA;
                border-radius: 6px;
                padding: 6px;
                font-size: 12px;
            }
        """)
        self.error_label.setVisible(False)
        layout.addWidget(self.error_label)

        # --- Form Fields ---
        form_layout = QFormLayout()
        form_layout.setSpacing(12)

        self.company_input = QLineEdit()
        self.company_input.setPlaceholderText("e.g. Google, Microsoft")

        self.position_input = QLineEdit()
        self.position_input.setPlaceholderText("e.g. Backend Engineer")

        self.date_input = QDateEdit()
        self.date_input.setDate(QDate.currentDate())
        self.date_input.setCalendarPopup(True)
        self.date_input.setDisplayFormat("yyyy-MM-dd")

        self.status_input = QComboBox()
        self.status_input.addItems(["Applied", "Interview", "Offer", "Rejected", "Withdrawn"])

        form_layout.addRow("🏢 Company:", self.company_input)
        form_layout.addRow("💼 Position:", self.position_input)
        form_layout.addRow("📅 Date:", self.date_input)
        form_layout.addRow("📊 Status:", self.status_input)
        layout.addLayout(form_layout)

        # --- Buttons ---
        button_layout = QHBoxLayout()
        button_layout.addStretch(1)

        self.btn_cancel = QPushButton("Cancel")
        self.btn_save = QPushButton("Save")
        self.btn_save.setObjectName("SaveButton")

        self.btn_cancel.clicked.connect(self.reject)
        self.btn_save.clicked.connect(self._on_save_clicked)

        button_layout.addWidget(self.btn_cancel)
        button_layout.addWidget(self.btn_save)
        layout.addSpacing(10)
        layout.addLayout(button_layout)

        # --- Modern Style ---
        self.setStyleSheet("""
            QDialog {
                background-color: #FFFFFF;
                border-radius: 12px;
            }

            QLabel {
                font-size: 15px;
                color: #000000;
            }

            QLineEdit, QDateEdit, QComboBox {
                border: 1px solid #BDC3C7;
                border-radius: 6px;
                padding: 6px 8px;
                font-size: 13px;
                color: #000000;
                background-color: #F8F9FA;
            }

            QLineEdit:focus, QDateEdit:focus, QComboBox:focus {
                border: 1px solid #3498DB;
                background-color: #FFFFFF;
            }

            QComboBox {
                padding-left: 6px;
            }

            QPushButton {
                border: none;
                border-radius: 6px;
                padding: 8px 14px;
                font-size: 13px;
                font-weight: 600;
                color: #000000;
            }

            QPushButton:hover {
                opacity: 0.9;
            }

            QPushButton#SaveButton {
                background-color: #3498DB;
                color: #FFFFFF;
            }

            QPushButton#SaveButton:hover {
                background-color: #2980B9;
            }

            QPushButton:not(#SaveButton) {
                background-color: #ECF0F1;
            }

            QPushButton:not(#SaveButton):hover {
                background-color: #D5DBDB;
            }
        """)

    # --- VALIDATION LOGIC ---
    def _on_save_clicked(self):
        company = self.company_input.text().strip()
        position = self.position_input.text().strip()

        # Reset previous error state
        self.error_label.setVisible(False)
        self.company_input.setStyleSheet("")
        self.position_input.setStyleSheet("")

        errors = []
        if not company:
            errors.append("Company field cannot be empty.")
            self.company_input.setStyleSheet("border: 1px solid #E74C3C;")
        if not position:
            errors.append("Position field cannot be empty.")
            self.position_input.setStyleSheet("border: 1px solid #E74C3C;")

        if errors:
            self.error_label.setText("⚠️ " + " ".join(errors))
            self.error_label.setVisible(True)
            return  # stop execution

        # If valid
        self.accept()

    def get_data(self):
        return {
            "company": self.company_input.text(),
            "position": self.position_input.text(),
            "date": self.date_input.date().toString("yyyy-MM-dd"),
            "status": self.status_input.currentText()
        }
