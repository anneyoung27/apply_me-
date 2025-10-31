from PySide6.QtWidgets import (
    QMainWindow, QToolBar, QLineEdit, QComboBox, QListWidget,
    QTableView, QGroupBox, QLabel, QTextEdit, QVBoxLayout, QHBoxLayout, QWidget, QPushButton
)
from PySide6.QtGui import QAction

# Add form
from app.add_dialog import ApplicationDialog
from app.database import SessionLocal
from app.models import Application
from PySide6.QtWidgets import QMessageBox
from PySide6.QtGui import QStandardItemModel, QStandardItem


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Apply Me — Job Tracker")
        self.resize(1200, 700)
        self.session = SessionLocal()  # buat koneksi database
        self.initUI()
        self.load_data()

    # Add form
    def open_add_form(self):
        dialog = ApplicationDialog(self.session)
        if dialog.exec_():  # jika ditekan Save
            self.load_data()  # reload tabel
            QMessageBox.information(self, "Success", "Application added successfully.")

    # Edit form
    def open_edit_form(self, selected_app):
        session = SessionLocal()
        dialog = ApplicationDialog(session, application=selected_app)
        if dialog.exec_():
            self.refresh_table()

    def load_data(self):
        # Ambil semua data lamaran
        apps = self.session.query(Application).order_by(Application.created_at.desc()).all()

        # Buat model untuk QTableView
        model = QStandardItemModel()
        model.setHorizontalHeaderLabels([
            "Company", "Position", "Location", "Date Applied", "Status", "Source"
        ])

        for app in apps:
            row = [
                QStandardItem(app.company_name or ""),
                QStandardItem(app.position or ""),
                QStandardItem(app.location or ""),
                QStandardItem(str(app.date_applied) if app.date_applied else ""),
                QStandardItem(app.status or ""),
                QStandardItem(app.source or "")
            ]
            for item in row:
                item.setEditable(False)
            model.appendRow(row)

        self.table.setModel(model)
        self.table.resizeColumnsToContents()
        self.table.horizontalHeader().setStretchLastSection(True)


    def initUI(self):
        # === Toolbar ===
        toolbar = QToolBar("Main Toolbar")
        self.addToolBar(toolbar)
        toolbar.setMovable(False)

        add_action = QAction("Add", self)
        import_action = QAction("Import", self)
        export_action = QAction("Export", self)
        settings_action = QAction("Settings", self)

        toolbar.addActions([add_action, import_action, export_action, settings_action])

        # Hubungkan tombol Add ke fungsi
        add_action.triggered.connect(self.open_add_form)

        # === Search & Filter Bar ===
        search_bar = QLineEdit()
        search_bar.setPlaceholderText("Search company or position...")
        filter_dropdown = QComboBox()
        filter_dropdown.addItems(["All", "Applied", "Interview", "Offer", "Rejected", "Withdrawn"])

        toolbar.addWidget(search_bar)
        toolbar.addWidget(filter_dropdown)

        # === Layouts ===
        left_pane = QListWidget()
        left_pane.addItems(["All", "Applied", "Phone Screen", "Interview", "Offer", "Rejected", "Withdrawn"])
        left_pane.setFixedWidth(150)

        self.table = QTableView()
        self.table.setSortingEnabled(True)

        # Right Panel — Detail Preview
        right_box = QGroupBox("Application Details")
        self.detail_company = QLabel("Company: -")
        self.detail_position = QLabel("Position: -")
        self.detail_notes = QTextEdit()
        self.detail_notes.setReadOnly(True)
        self.open_resume_button = QPushButton("Open Resume")
        self.open_cover_button = QPushButton("Open Cover Letter")

        vbox = QVBoxLayout()
        vbox.addWidget(self.detail_company)
        vbox.addWidget(self.detail_position)
        vbox.addWidget(QLabel("Notes:"))
        vbox.addWidget(self.detail_notes)
        vbox.addWidget(self.open_resume_button)
        vbox.addWidget(self.open_cover_button)
        right_box.setLayout(vbox)
        right_box.setFixedWidth(300)

        # === Central Layout ===
        main_layout = QHBoxLayout()
        main_layout.addWidget(left_pane)
        main_layout.addWidget(self.table)
        main_layout.addWidget(right_box)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

