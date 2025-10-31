from PySide6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QVBoxLayout,
    QTableView, QListWidget, QListWidgetItem,
    QToolBar, QLineEdit, QComboBox, QLabel,
    QStackedWidget, QPushButton, QGroupBox, QTextEdit, QMessageBox
)
from PySide6.QtGui import QAction, QStandardItemModel, QStandardItem
from PySide6.QtCore import Qt

# App imports
from app.add_dialog import ApplicationDialog
from app.database import SessionLocal
from app.models import Application


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
        self.table.setColumnWidth(0, 100)  # Company
        self.table.setColumnWidth(1, 100)  # Position
        self.table.setColumnWidth(2, 120)  # Location
        self.table.setColumnWidth(3, 80)  # Date Applied
        self.table.setColumnWidth(4, 90)  # Status
        self.table.horizontalHeader().setStretchLastSection(True)

    # === Switch Page ===
    def switch_page(self, index):
        self.pages.setCurrentIndex(index)

    # === Init UI ===
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
        add_action.triggered.connect(self.open_add_form)

        # === Side Menu ===
        self.side_menu = QListWidget()
        self.side_menu.setFixedWidth(180)
        self.side_menu.addItem(QListWidgetItem("🏠 Dashboard"))
        self.side_menu.addItem(QListWidgetItem("📊 Statistics"))
        self.side_menu.currentRowChanged.connect(self.switch_page)

        # === Pages Container ===
        self.pages = QStackedWidget()

        # =======================
        # Page 1 — DASHBOARD
        # =======================
        self.dashboard_page = QWidget()
        dashboard_layout = QHBoxLayout(self.dashboard_page)

        # Center (Table + filter bar)
        center_layout = QVBoxLayout()
        search_bar = QLineEdit()
        search_bar.setPlaceholderText("Search company or position...")
        filter_dropdown = QComboBox()
        filter_dropdown.addItems(["All", "Applied", "Interview", "Offer", "Rejected", "Withdrawn"])

        filter_layout = QHBoxLayout()
        filter_layout.addWidget(search_bar)
        filter_layout.addWidget(filter_dropdown)

        self.table = QTableView()
        self.table.setSortingEnabled(True)

        center_layout.addLayout(filter_layout)
        center_layout.addWidget(self.table)

        # Right Pane (Details)
        right_box = QGroupBox("Application Details")
        vbox = QVBoxLayout(right_box)
        self.detail_company = QLabel("Company: -")
        self.detail_position = QLabel("Position: -")
        self.detail_notes = QTextEdit()
        self.detail_notes.setReadOnly(True)
        self.open_resume_button = QPushButton("Open Resume")
        self.open_cover_button = QPushButton("Open Cover Letter")
        vbox.addWidget(self.detail_company)
        vbox.addWidget(self.detail_position)
        vbox.addWidget(QLabel("Notes:"))
        vbox.addWidget(self.detail_notes)
        vbox.addWidget(self.open_resume_button)
        vbox.addWidget(self.open_cover_button)
        right_box.setFixedWidth(300)

        # Combine Dashboard Layout
        dashboard_layout.addLayout(center_layout)
        dashboard_layout.addWidget(right_box)

        # =======================
        # Page 2 — STATISTICS
        # =======================
        self.stats_page = QWidget()
        stats_layout = QVBoxLayout(self.stats_page)
        stats_layout.addWidget(QLabel("📊 Statistics Page — Coming Soon..."))

        # Add pages to stack
        self.pages.addWidget(self.dashboard_page)
        self.pages.addWidget(self.stats_page)

        # === Root Layout ===
        root_layout = QHBoxLayout()
        root_layout.addWidget(self.side_menu)
        root_layout.addWidget(self.pages)

        container = QWidget()
        container.setLayout(root_layout)
        self.setCentralWidget(container)

        # Default ke Dashboard
        self.side_menu.setCurrentRow(0)
