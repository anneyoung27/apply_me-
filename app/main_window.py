from PySide6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QVBoxLayout,
    QTableView, QListWidget, QListWidgetItem,
    QToolBar, QLineEdit, QComboBox, QLabel,
    QStackedWidget, QPushButton, QGroupBox, QTextEdit, QMessageBox
)
from PySide6.QtGui import QAction, QStandardItemModel, QStandardItem, QFont
from PySide6.QtCore import Qt

# App imports
from app.add_dialog import ApplicationDialog
from app.database import SessionLocal
from app.models import Application
from app.utils import open_file as utils_open_file
from importlib import import_module


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Apply Me — Job Tracker")
        self.resize(1200, 700)
        self.session = SessionLocal()

        self.initUI()
        self.load_data()

    # === Add form ===
    def open_add_form(self):
        dialog = ApplicationDialog(self.session)
        if dialog.exec_():
            self.load_data()
            QMessageBox.information(self, "Success", "Application added successfully.")

    # === Edit form ===
    def open_edit_form(self, selected_app):
        dialog = ApplicationDialog(self.session, application=selected_app)
        if dialog.exec_():
            self.load_data()

    # === Load data to table ===
    def load_data(self):
        apps = self.session.query(Application).order_by(Application.created_at.desc()).all()

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

        # Saat baris di tabel diklik, tampilkan detail
        self.table.selectionModel().selectionChanged.connect(self.show_application_details)

        self.table.clicked.connect(self.show_application_details)

        self.table.setColumnWidth(0, 100)  # Company
        self.table.setColumnWidth(1, 100)  # Position
        self.table.setColumnWidth(2, 120)  # Location
        self.table.setColumnWidth(3, 80)  # Date Applied
        self.table.setColumnWidth(4, 90)  # Status
        self.table.horizontalHeader().setStretchLastSection(True)

        self.search_applications()

    # === Search method ===
    def search_applications(self):
        if not hasattr(self, "search_bar") or not hasattr(self, "filter_dropdown"):
            return  # Pastikan widget sudah ada

        search_text = self.search_bar.text().strip().lower()
        selected_status = self.filter_dropdown.currentText()

        # Query dasar
        query = self.session.query(Application)

        # Filter berdasarkan status
        if selected_status != "All":
            query = query.filter(Application.status == selected_status)

        # Filter berdasarkan teks pencarian
        if search_text:
            query = query.filter(
                (Application.company_name.ilike(f"%{search_text}%")) |
                (Application.position.ilike(f"%{search_text}%"))
            )

        apps = query.order_by(Application.created_at.desc()).all()

        # === Bangun ulang tabel ===
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

        # Lebar kolom stabil
        self.table.setColumnWidth(0, 100)  # Company
        self.table.setColumnWidth(1, 100)  # Position
        self.table.setColumnWidth(2, 120)  # Location
        self.table.setColumnWidth(3, 80)  # Date Applied
        self.table.setColumnWidth(4, 90)  # Status
        self.table.horizontalHeader().setStretchLastSection(True)

    # === Detail panel ===
    def show_application_details(self, index):
        """Tampilkan detail lamaran di panel kanan saat user klik di tabel"""
        if not index.isValid():
            return

        # Ambil baris yang diklik
        row = index.row()
        company = self.table.model().item(row, 0).text()  # Kolom Company
        position = self.table.model().item(row, 1).text()  # Kolom Position
        location = self.table.model().item(row, 2).text() # Kolom Location
        status = self.table.model().item(row, 4).text() # Kolom Status

        # Cari data lengkap di database
        app = (
            self.session.query(Application)
            .filter_by(company_name=company, position=position, location=location, status=status)
            .first()
        )

        if not app:
            return

        # Tampilkan ke panel kanan
        self.detail_company.setText(f"Company: {app.company_name}")
        self.detail_position.setText(f"Position: {app.position}")
        self.detail_location.setText(f"Location: {app.location}")
        self.detail_status.setText(f"Status: {app.status}")
        self.detail_notes.setPlainText(app.notes or "")

        # Simpan path file untuk tombol "Open"
        self.current_resume_path = app.resume_file
        self.current_cover_path = app.cover_letter_file

        # Aktifkan / nonaktifkan tombol sesuai file ada / tidak
        self.open_resume_button.setEnabled(bool(app.resume_file))
        self.open_cover_button.setEnabled(bool(app.cover_letter_file))

    # === Switch Page ===
    def switch_page(self, index):
        self.pages.setCurrentIndex(index)

    # === Init UI ===
    def initUI(self):
        # --- Toolbar ---
        toolbar = QToolBar("Main Toolbar")
        self.addToolBar(toolbar)
        toolbar.setMovable(False)

        add_action = QAction("Add", self)
        import_action = QAction("Import", self)
        export_action = QAction("Export", self)
        settings_action = QAction("Settings", self)

        toolbar.addActions([add_action, import_action, export_action, settings_action])
        add_action.triggered.connect(self.open_add_form)

        # --- Central Layout ---
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)

        # === Side Menu ===
        self.side_menu = QListWidget()
        self.side_menu.setFixedWidth(180)
        self.side_menu.addItem(QListWidgetItem("🏠 Dashboard"))
        self.side_menu.addItem(QListWidgetItem("📊 Statistics"))
        self.side_menu.currentRowChanged.connect(self.switch_page)

        # === Pages Container ===
        self.pages = QStackedWidget()

        # === PAGE 1: Dashboard ===
        self.dashboard_page = QWidget()
        dashboard_main_layout = QHBoxLayout(self.dashboard_page)

        # --- Left (Table Area) ---
        left_layout = QVBoxLayout()

        # Header
        header_label = QLabel("MY JOB APPLICATION")
        header_font = QFont("Segoe UI", 16, QFont.Bold)
        header_label.setFont(header_font)
        header_label.setAlignment(Qt.AlignCenter)
        header_label.setStyleSheet("color: #EDEDED; margin-bottom: 10px;")

        # Search & Filter
        # === Search & Filter ===
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Search company or position...")
        self.search_bar.textChanged.connect(self.search_applications)  # Realtime search

        self.filter_dropdown = QComboBox()
        self.filter_dropdown.addItems(["All", "Applied", "Interview", "Offer", "Rejected", "Withdrawn"])
        self.filter_dropdown.currentTextChanged.connect(self.search_applications)

        search_filter_layout = QHBoxLayout()
        search_filter_layout.addWidget(self.search_bar)
        search_filter_layout.addWidget(self.filter_dropdown)

        # Table
        self.table = QTableView()
        self.table.setSortingEnabled(True)

        left_layout.addWidget(header_label)
        left_layout.addLayout(search_filter_layout)
        left_layout.addWidget(self.table)

        # --- Right (Detail Panel) ---
        right_box = QGroupBox("Application Details")
        self.detail_company = QLabel("Company: -")
        self.detail_position = QLabel("Position: -")
        self.detail_location = QLabel("Location: -")
        self.detail_status = QLabel("Status: -")
        self.detail_notes = QTextEdit()
        self.detail_notes.setReadOnly(True)

        self.open_resume_button = QPushButton("Open Resume")
        self.open_resume_button.setEnabled(False)
        self.open_cover_button = QPushButton("Open Cover Letter")
        self.open_cover_button.setEnabled(False)

        # Hubungkan tombol file
        self.open_resume_button.clicked.connect(
            lambda: import_module("app.utils").open_file(getattr(self, "current_resume_path", None))
        )
        self.open_cover_button.clicked.connect(
            lambda: import_module("app.utils").open_file(getattr(self, "current_cover_path", None))
        )
        vbox = QVBoxLayout()
        vbox.addWidget(self.detail_company)
        vbox.addWidget(self.detail_position)
        vbox.addWidget(self.detail_location)
        vbox.addWidget(self.detail_status)
        vbox.addWidget(QLabel("Notes:"))
        vbox.addWidget(self.detail_notes)
        vbox.addWidget(self.open_resume_button)
        vbox.addWidget(self.open_cover_button)
        right_box.setLayout(vbox)
        right_box.setFixedWidth(300)

        # Combine left & right
        dashboard_main_layout.addLayout(left_layout)
        dashboard_main_layout.addWidget(right_box)

        # === PAGE 2: Statistics ===
        self.stats_page = QWidget()
        stats_layout = QVBoxLayout(self.stats_page)
        stats_label = QLabel("📊 Statistics Page — coming soon...")
        stats_label.setAlignment(Qt.AlignCenter)
        stats_label.setStyleSheet("font-size: 14px; color: #555;")
        stats_layout.addWidget(stats_label)

        # Tambahkan ke stacked widget
        self.pages.addWidget(self.dashboard_page)
        self.pages.addWidget(self.stats_page)

        # Gabungkan Side Menu + Pages
        main_layout.addWidget(self.side_menu)
        main_layout.addWidget(self.pages)

        self.side_menu.setCurrentRow(0)
