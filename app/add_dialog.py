from PySide6.QtWidgets import (
    QDialog, QLineEdit, QTextEdit, QComboBox, QDateEdit,
    QLabel, QPushButton, QFileDialog, QGridLayout, QHBoxLayout, QVBoxLayout
)

from PySide6.QtGui import QIcon
from app.utils import qdate_to_date
from app.models import Application

class ApplicationDialog(QDialog):
    def __init__(self, session, application=None, parent=None):
        super().__init__(parent)
        self.session = session
        self.application = application
        self.resume_path = None
        self.cover_path = None

        if application:
            self.setWindowTitle("Edit Application")
            self.setWindowIcon(QIcon("assets/others_icon/edit_form.png"))
        else:
            self.setWindowTitle("Add Application")
            self.setWindowIcon(QIcon("assets/others_icon/add_new_form.png"))

        self.resize(500, 600)
        self.initUI()

        if application:
            self.load_data()

    def initUI(self):
        layout = QGridLayout()

        # === Input Fields ===
        self.company_input = QLineEdit()
        self.position_input = QLineEdit()
        self.location_input = QLineEdit()

        self.date_input = QDateEdit()
        self.date_input.setCalendarPopup(True)
        self.date_input.setDisplayFormat("dd/MM/yyyy")
        self.date_input.setDate(qdate_to_date(self.date_input.date().currentDate()))

        self.source_input = QLineEdit()
        self.status_input = QComboBox()
        self.status_input.addItems(["Applied", "Phone Screen", "Interview", "Offer", "Rejected", "Withdrawn"])

        self.salary_input = QLineEdit()
        self.notes_input = QTextEdit()

        # === Attach Files ===
        self.resume_label = QLabel("No file selected")
        self.cover_label = QLabel("No file selected")
        self.resume_button = QPushButton("Attach Resume")
        self.cover_button = QPushButton("Attach Cover Letter")

        self.resume_button.clicked.connect(self.attach_resume)
        self.cover_button.clicked.connect(self.attach_cover)

        # === Buttons ===
        self.save_button = QPushButton("Save")
        self.cancel_button = QPushButton("Cancel")

        self.save_button.clicked.connect(self.save_data)
        self.cancel_button.clicked.connect(self.reject)

        # === Layout Grid ===
        layout.addWidget(QLabel("Company:"), 0, 0)
        layout.addWidget(self.company_input, 0, 1)

        layout.addWidget(QLabel("Position:"), 1, 0)
        layout.addWidget(self.position_input, 1, 1)

        layout.addWidget(QLabel("Location:"), 2, 0)
        layout.addWidget(self.location_input, 2, 1)

        layout.addWidget(QLabel("Date Applied:"), 3, 0)
        layout.addWidget(self.date_input, 3, 1)

        layout.addWidget(QLabel("Source:"), 4, 0)
        layout.addWidget(self.source_input, 4, 1)

        layout.addWidget(QLabel("Status:"), 5, 0)
        layout.addWidget(self.status_input, 5, 1)

        layout.addWidget(QLabel("Salary Expectation:"), 6, 0)
        layout.addWidget(self.salary_input, 6, 1)

        layout.addWidget(QLabel("Notes:"), 7, 0)
        layout.addWidget(self.notes_input, 7, 1)

        # === Resume / Cover Section ===
        layout.addWidget(QLabel("Resume File:"), 8, 0)
        layout.addWidget(self.resume_label, 8, 1)
        layout.addWidget(self.resume_button, 8, 2)

        layout.addWidget(QLabel("Cover Letter:"), 9, 0)
        layout.addWidget(self.cover_label, 9, 1)
        layout.addWidget(self.cover_button, 9, 2)

        # === Buttons Layout ===
        btn_layout = QHBoxLayout()
        btn_layout.addWidget(self.save_button)
        btn_layout.addWidget(self.cancel_button)

        # === Main Vertical Layout ===
        main_layout = QVBoxLayout()
        main_layout.addLayout(layout)
        main_layout.addLayout(btn_layout)
        self.setLayout(main_layout)

    # === Load existing data for Edit mode ===
    def load_data(self):
        app = self.application
        self.company_input.setText(app.company_name or "")
        self.position_input.setText(app.position or "")
        self.location_input.setText(app.location or "")
        if app.date_applied:
            qd = qdate_to_date(self.date_input.date())
            self.date_input.setDate(qd)
        self.source_input.setText(app.source or "")
        if app.status:
            idx = self.status_input.findText(app.status)
            if idx >= 0:
                self.status_input.setCurrentIndex(idx)
        self.salary_input.setText(app.salary_expectation or "")
        self.notes_input.setPlainText(app.notes or "")
        if app.resume_file:
            self.resume_label.setText(app.resume_file)
            self.resume_path = app.resume_file
        if app.cover_letter_file:
            self.cover_label.setText(app.cover_letter_file)
            self.cover_path = app.cover_letter_file

    # === File Attach Handlers ===
    def attach_resume(self):
        path, _ = QFileDialog.getOpenFileName(self, "Select Resume File", "", "PDF Files (*.pdf);;All Files (*)")
        if path:
            self.resume_path = path
            self.resume_label.setText(path.split("/")[-1])

    def attach_cover(self):
        path, _ = QFileDialog.getOpenFileName(self, "Select Cover Letter File", "", "PDF Files (*.pdf);;All Files (*)")
        if path:
            self.cover_path = path
            self.cover_label.setText(path.split("/")[-1])

    # === Save Handler ===
    def save_data(self):
        from PySide6.QtWidgets import QMessageBox
        from datetime import datetime
        from app.models import StatusHistory  # pastikan ini sesuai path kamu

        company = self.company_input.text().strip()
        position = self.position_input.text().strip()

        if not company or not position:
            QMessageBox.warning(self, "Error", "Company name and position are required.")
            return

        if self.application:
            # === Edit mode ===
            app = self.application
            old_status = app.status  # Simpan status lama sebelum diubah
        else:
            # === Add mode ===
            app = Application()

            # === Generate custom ID (e.g. TO001, TO002) ===
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

            app.id = f"{prefix}{new_num:03d}"
            self.session.add(app)
            old_status = None  # Tidak ada status lama karena data baru

        # === Simpan data ke Application ===
        app.company_name = company
        app.position = position
        app.location = self.location_input.text().strip()
        app.date_applied = qdate_to_date(self.date_input.date().currentDate())
        app.source = self.source_input.text().strip()
        new_status = self.status_input.currentText()
        app.status = new_status
        app.salary_expectation = self.salary_input.text().strip()
        app.notes = self.notes_input.toPlainText().strip()
        app.resume_file = self.resume_path
        app.cover_letter_file = self.cover_path

        # === Commit dulu untuk pastikan ID tersimpan ===
        self.session.commit()

        # === Tambahkan ke StatusHistory ===
        # Jika data baru, tambahkan entri awal
        if not self.application:
            history = StatusHistory(
                application_id=app.id,
                old_status=None,
                new_status=new_status,
                timestamp=datetime.now()
            )
            self.session.add(history)

        # Jika edit dan status berubah, simpan perubahan ke history
        elif old_status != new_status:
            history = StatusHistory(
                application_id=app.id,
                old_status=old_status,
                new_status=new_status,
                timestamp=datetime.now()
            )
            self.session.add(history)

        # === Simpan semua ke DB ===
        self.session.commit()
        self.accept()
