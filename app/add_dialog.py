from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QFormLayout, QLineEdit, QDialogButtonBox,
    QComboBox, QDateEdit, QSpinBox, QTextEdit, QPushButton, QFileDialog,
    QHBoxLayout, QLabel, QMessageBox
)
from PySide6.QtCore import QDate, Qt
from PySide6.QtGui import QFont


class AddDialog(QDialog):
    def __init__(self, parent=None):  # ← tambahkan parent
        super().__init__(parent)
        self.setWindowTitle("Add New Application")
        self.resize(450, 650)

        # === Dark modern style ===
        self.setStyleSheet("""
            QDialog {
                background-color: #121212;
                color: #FFFFFF;
                font-family: 'Segoe UI';
                font-size: 11pt;
            }
            QLabel {
                font-weight: 500;
                color: #FFFFFF;
            }
            QLineEdit, QComboBox, QDateEdit, QSpinBox, QTextEdit {
                background-color: #1E1E1E;
                color: #FFFFFF;
                border: 1px solid #3A3A3A;
                border-radius: 8px;
                padding: 6px;
                selection-background-color: #0078D7;
            }
            QLineEdit:focus, QComboBox:focus, QDateEdit:focus, QTextEdit:focus {
                border: 1px solid #0078D7;
            }
            QPushButton {
                background-color: #0078D7;
                color: white;
                border-radius: 8px;
                padding: 6px 14px;
                font-weight: 500;
            }
            QPushButton:hover {
                background-color: #0A84FF;
            }
            QDialogButtonBox QPushButton {
                background-color: #0078D7;
                color: white;
                border-radius: 6px;
                padding: 6px 12px;
            }
            QDialogButtonBox QPushButton:hover {
                background-color: #0A84FF;
            }
        """)

        layout = QVBoxLayout(self)

        # === Header ===
        header = QLabel("Add New Application")
        header.setFont(QFont("Segoe UI", 14, QFont.Bold))
        header.setAlignment(Qt.AlignCenter)
        header.setStyleSheet("color: #FFFFFF; margin-bottom: 15px;")
        layout.addWidget(header)

        # === Form Layout ===
        form = QFormLayout()
        form.setSpacing(10)

        self.company_input = QLineEdit()
        self.position_input = QLineEdit()
        self.location_input = QLineEdit()

        self.date_input = QDateEdit()
        self.date_input.setDate(QDate.currentDate())
        self.date_input.setCalendarPopup(True)

        self.source_input = QLineEdit()

        self.status_input = QComboBox()
        self.status_input.addItems([
            "Applied", "Interview", "Offer", "Rejected", "Hired"
        ])

        self.salary_input = QSpinBox()
        self.salary_input.setRange(0, 100000000)
        self.salary_input.setSuffix(" IDR")

        self.notes_input = QTextEdit()
        self.notes_input.setPlaceholderText("Add notes or comments here...")

        # File pickers
        self.resume_input = QLineEdit()
        self.resume_button = QPushButton("Browse")
        self.resume_button.clicked.connect(lambda: self.browse_file(self.resume_input))

        self.cover_input = QLineEdit()
        self.cover_button = QPushButton("Browse")
        self.cover_button.clicked.connect(lambda: self.browse_file(self.cover_input))

        resume_layout = QHBoxLayout()
        resume_layout.addWidget(self.resume_input)
        resume_layout.addWidget(self.resume_button)

        cover_layout = QHBoxLayout()
        cover_layout.addWidget(self.cover_input)
        cover_layout.addWidget(self.cover_button)

        # Tambahkan semua field ke form
        form.addRow("Company", self.company_input)
        form.addRow("Position", self.position_input)
        form.addRow("Location", self.location_input)
        form.addRow("Date Applied", self.date_input)
        form.addRow("Source", self.source_input)
        form.addRow("Status", self.status_input)
        form.addRow("Salary Expectation", self.salary_input)
        form.addRow("Notes", self.notes_input)
        form.addRow("Resume File", resume_layout)
        form.addRow("Cover Letter", cover_layout)

        layout.addLayout(form)

        # === Tombol OK / Cancel ===
        self.button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.button_box.accepted.connect(self.validate_and_accept)
        self.button_box.rejected.connect(self.reject)
        layout.addWidget(self.button_box)

    def browse_file(self, target_input: QLineEdit):
        """Buka file dialog untuk memilih file"""
        file_path, _ = QFileDialog.getOpenFileName(self, "Select File", "", "All Files (*)")
        if file_path:
            target_input.setText(file_path)

    def validate_and_accept(self):
        """Validasi field wajib"""
        if not self.company_input.text().strip():
            self.show_error("Company field is required.")
            return
        if not self.position_input.text().strip():
            self.show_error("Position field is required.")
            return

        self.accept()

    def show_error(self, message):
        QMessageBox.warning(self, "Validation Error", message)

    def get_data(self):
        """Ambil data dari form"""
        return {
            "company": self.company_input.text().strip(),
            "position": self.position_input.text().strip(),
            "location": self.location_input.text().strip(),
            "date": self.date_input.date().toString("yyyy-MM-dd"),
            "source": self.source_input.text().strip(),
            "status": self.status_input.currentText(),
            "salary_expectation": self.salary_input.value(),
            "notes": self.notes_input.toPlainText().strip(),
            "resume_file": self.resume_input.text().strip(),
            "cover_letter_file": self.cover_input.text().strip()
        }
