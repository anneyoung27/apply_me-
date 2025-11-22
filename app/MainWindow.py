from PySide6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QVBoxLayout,
    QTableView,
    QToolBar, QLineEdit, QComboBox, QLabel,
    QStackedWidget, QPushButton, QGroupBox, QTextEdit, QMessageBox, QMenu, QToolButton
)
from PySide6.QtGui import QAction, QStandardItemModel, QStandardItem, QFont, QIcon
from PySide6.QtCore import Qt, QSize, QTimer

# App imports
from app.add_feature.AddDialog import ApplicationDialog
from app.database.Database import SessionLocal
from app.database.Models import Application
from app.import_feature.ImportFormatWindow import ImporterWindow
from app.export_feature.ExporterMenu import DataExporter
from datetime import datetime


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Apply Me — Job Tracker")
        self.resize(1200, 700)

        # Nonaktifkan tombol maximize
        self.setFixedSize(self.width(), self.height())

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
                QStandardItem(app.formatted_date),
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
        self.table.setColumnWidth(0, 95)  # Company
        self.table.setColumnWidth(1, 120)  # Position
        self.table.setColumnWidth(2, 100)  # Location
        self.table.setColumnWidth(3, 85)  # Date Applied
        self.table.setColumnWidth(4, 70)  # Status
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

    # === Right click feature to Edit and Delete
    def open_context_menu(self, position):
        index = self.table.indexAt(position)
        if not index.isValid():
            return

        menu = QMenu()
        menu.setStyleSheet("""
            QMenu::item {
                padding-left: 12px;   /* default biasanya 20px, kurangi */
                padding-right: 10px;
            }
            QMenu {
                margin: 5px;         /* hilangkan margin tambahan */
            }
        """)
        edit_action = menu.addAction("✏️  Edit")
        delete_action = menu.addAction("🗑️  Delete")

        action = menu.exec_(self.table.viewport().mapToGlobal(position))

        if action == edit_action:
            self.edit_selected_application(index.row())
        elif action == delete_action:
            self.delete_selected_application(index.row())

    def get_application_by_row(self, row):
        """Ambil Application dari database berdasarkan baris yang diklik."""
        company = self.table.model().item(row, 0).text()
        position = self.table.model().item(row, 1).text()
        return (
            self.session.query(Application)
            .filter_by(company_name=company, position=position)
            .first()
        )

    def edit_selected_application(self, row):
        """Buka dialog edit untuk data yang dipilih."""
        app = self.get_application_by_row(row)
        if not app:
            QMessageBox.warning(self, "Not Found", "Application not found in database.")
            return

        dialog = ApplicationDialog(self.session, application=app)
        if dialog.exec_():
            app.updated_at = datetime.now() # Jika ada update pada row, maka update UPDATED_AT
            self.session.commit()
            self.load_data()
            QMessageBox.information(self, "Updated", "Application updated successfully.")

    def delete_selected_application(self, row):
        """Hapus data dari database."""
        app = self.get_application_by_row(row)
        if not app:
            QMessageBox.warning(self, "Not Found", "Application not found in database.")
            return

        confirm = QMessageBox.question(
            self,
            "Delete Confirmation",
            f"Are you sure you want to delete application for '{app.company_name}'?",
            QMessageBox.Yes | QMessageBox.No,
        )
        if confirm == QMessageBox.Yes:
            self.session.delete(app)
            self.session.commit()
            self.load_data()
            QMessageBox.information(self, "Deleted", "Application deleted successfully.")

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
        about_action = QAction("About", self)

        toolbar.addActions([add_action, import_action, about_action])
        add_action.triggered.connect(self.open_add_form) # ADD DATA ACTION

        # === EXPORT ACTION AND SUB MENU ===
        export_button = QToolButton()
        export_button.setText("Export")
        export_button.setPopupMode(QToolButton.MenuButtonPopup)
        export_button.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        export_button.setStyleSheet("padding-left: 15px; qproperty-iconSize: 18px")

        # === EXPORT - SUB MENU ===
        export_menu = QMenu(export_button)
        to_csv_action = export_menu.addAction("Export to CSV")
        to_csv_action.setIcon(QIcon("assets/head_menu/csv-file.png"))
        to_excel_action = export_menu.addAction("Export to Excel")
        to_excel_action.setIcon(QIcon("assets/head_menu/xlsx-file.png"))
        export_menu.setStyleSheet("""
                    QMenu::item {
                        padding-left: 12px;    /* default biasanya 20px, kurangi */
                        padding-right: 10px;
                    }
                    QMenu {
                        margin: 8px;           /* hilangkan margin tambahan */
                    }
                """)
        export_button.setMenu(export_menu)

        # === EXPORTER CLASS ===
        exporter = DataExporter(self.session, Application)
        to_csv_action.triggered.connect(lambda: exporter.export_to_csv(self))
        to_excel_action.triggered.connect(lambda: exporter.export_to_excel(self))

        # === SETTINGS ACTION AND SUB MENU ===
        setting_button = QToolButton()
        setting_button.setText("Preferences")
        setting_button.setPopupMode(QToolButton.MenuButtonPopup)
        setting_button.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        setting_button.setStyleSheet("padding-left: 15px; qproperty-iconSize: 18px")

        setting_menu = QMenu(setting_button)

        database_management = setting_menu.addAction("Database Management")
        database_management.setIcon(QIcon("assets/head_menu/database_management.png"))
        data_management = setting_menu.addAction("Data Management")
        data_management.setIcon(QIcon("assets/head_menu/data_management.png"))
        notification_and_reminders = setting_menu.addAction("Notification and Reminders")
        notification_and_reminders.setIcon(QIcon("assets/head_menu/notification.png"))
        advanced_setting = setting_menu.addAction("Advanced Setting")
        advanced_setting.setIcon(QIcon("assets/head_menu/advanced-setting.png"))
        setting_menu.setStyleSheet("""
                            QMenu::item {
                                padding-left: 12px;    /* default biasanya 20px, kurangi */
                                padding-right: 10px;
                            }
                            QMenu {
                                margin: 8px;           /* hilangkan margin tambahan */
                            }
                        """)
        setting_button.setMenu(setting_menu)


        # === MASUKKAN KE TOOLBAR ===
        toolbar.addAction(add_action)
        toolbar.addAction(import_action)
        toolbar.addWidget(export_button)
        toolbar.addWidget(setting_button)
        toolbar.addAction(about_action)

        # === IMPORT ACTION ===
        import_action.triggered.connect(lambda: ImporterWindow.open_importer_window(self))

        # --- Central Layout ---
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)

        # === SIDE MENU CONTAINER (dengan border kanan) ===
        self.side_menu_container = QWidget()
        container_layout = QVBoxLayout(self.side_menu_container)
        container_layout.setContentsMargins(0, 0, 0, 0)
        container_layout.setSpacing(0)

        self.side_menu_container.setStyleSheet("""
            QWidget {
                background-color: #212121;
                border-right: 1px solid #FFFFFF;
            }
        """)

        # === Side Menu ===
        self.side_menu = QWidget()
        side_layout = QVBoxLayout(self.side_menu)
        side_layout.setContentsMargins(0, 0, 0, 0)
        side_layout.setSpacing(0)
        self.side_menu.setFixedWidth(180)

        self.side_menu.setStyleSheet("""
            QPushButton {
                text-align: left;
                padding: 10px 16px;
                font-size: 13px;
                color: #dddddd;
                border: none;
                background-color: transparent;
            }
            QPushButton:hover {
                background-color: #1f1f1f;
                color: #ffffff;
            }
            QPushButton:checked {
                background-color: #2563eb;
                color: white;
                font-weight: bold;
                border-right: none; /* Pastikan border tidak muncul di tombol aktif */
            }
        """)

        # Tombol menu dengan ikon
        btn_dashboard = QPushButton("  Dashboard")
        btn_dashboard.setIcon(QIcon("assets/side_menu/home.png"))
        btn_dashboard.setIconSize(QSize(18, 18))

        btn_stats = QPushButton("  Statistics")
        btn_stats.setIcon(QIcon("assets/side_menu/statistics.png"))
        btn_stats.setIconSize(QSize(18, 18))

        btn_reminders = QPushButton("  Reminders")
        btn_reminders.setIcon(QIcon("assets/side_menu/reminders.png"))
        btn_reminders.setIconSize(QSize(18, 18))

        btn_contacts = QPushButton("  Contacts")
        btn_contacts.setIcon(QIcon("assets/side_menu/contacts.png"))
        btn_contacts.setIconSize(QSize(18, 18))

        # Tambahkan tombol ke layout
        for btn in [btn_dashboard, btn_stats, btn_reminders, btn_contacts]:
            btn.setCheckable(True)
            side_layout.addWidget(btn)

        side_layout.addStretch()
        self.side_menu_container.setFixedWidth(180)

        container_layout.addWidget(self.side_menu)

        # === Hubungkan tombol ke halaman ===
        btn_dashboard.clicked.connect(lambda: self.pages.setCurrentWidget(self.home_page))
        btn_stats.clicked.connect(lambda: self.pages.setCurrentWidget(self.stats_page))
        btn_reminders.clicked.connect(lambda: self.pages.setCurrentWidget(self.reminders_page))
        btn_contacts.clicked.connect(lambda: self.pages.setCurrentWidget(self.contact_page))

        # === Buat agar tombol aktif (checked) berubah otomatis ===
        def set_active_button(active_button):
            for b in [btn_dashboard, btn_stats, btn_reminders, btn_contacts]:
                b.setChecked(b == active_button)

        btn_dashboard.clicked.connect(lambda: set_active_button(btn_dashboard))
        btn_stats.clicked.connect(lambda: set_active_button(btn_stats))
        btn_reminders.clicked.connect(lambda: set_active_button(btn_reminders))
        btn_contacts.clicked.connect(lambda: set_active_button(btn_contacts))

        # Default aktif: Dashboard
        btn_dashboard.setChecked(True)

        # === Pages Container ===
        self.pages = QStackedWidget()

        # === PAGE 1: Home ===
        self.home_page = QWidget()
        home_main_layout = QHBoxLayout(self.home_page)

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

        # === TABLE SETUP ===
        self.table = QTableView()
        self.table.setContextMenuPolicy(Qt.CustomContextMenu)  # aktifkan klik kanan
        self.table.customContextMenuRequested.connect(self.open_context_menu)
        self.table.setSortingEnabled(True)

        # Hapus kolom nomor (row header)
        self.table.verticalHeader().setVisible(False)

        # Opsional: agar kolom otomatis pas dan rapi
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.horizontalHeader().setDefaultSectionSize(160)

        # Styling agar lebih menyatu dengan tema gelap
        self.table.setStyleSheet("""
            QTableView {
                background-color: #1e1e1e;
                color: #ddd;
                gridline-color: #333;
                border: none;
                selection-background-color: #1565c0;
                selection-color: white;
            }
            QHeaderView::section {
                background-color: #2b2b2b;
                color: #ddd;
                padding: 4px;
                border: none;
            }
        """)

        # Tambahkan ke layout kiri
        left_layout.addWidget(header_label)
        left_layout.addLayout(search_filter_layout)
        left_layout.addWidget(self.table)

        # --- Right (APPLICATION DETAIL PANEL) ---
        right_container = QWidget()
        right_container.setFixedWidth(320)

        right_layout = QVBoxLayout(right_container)
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(6)

        # === REAL-TIME CLOCK (di atas panel) ===
        self.running_time_label = QLabel()
        self.running_time_label.setAlignment(Qt.AlignCenter)
        self.running_time_label.setStyleSheet("""
            font-size: 13px;
            color: #e0e0e0;
            background-color: #212121;
            padding: 6px 10px;
            border-bottom: 1px solid #333;
            border-top-left-radius: 6px;
            border-top-right-radius: 6px;
        """)

        def update_running_time():
            now = datetime.now()
            formatted = now.strftime("%A, %d %B %Y %H:%M:%S")
            self.running_time_label.setText(f"🕒 {formatted}")

        self.timer = QTimer(self)
        self.timer.timeout.connect(update_running_time)
        self.timer.start(1000)
        update_running_time()

        # === (Right) APPLICATION DETAILS BOX ===
        right_box = QGroupBox("Application Details")
        right_box.setStyleSheet("""
            QGroupBox {
                background-color: #212121;
                border: 1px solid #2e2e2e;
                border-radius: 8px;
                margin-top: 6px;
                color: #e0e0e0;
                font-weight: 600;
                font-size: 12.5px;
                padding-top: 12px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top left;
                padding: 0 8px;
                color: #FFFFFF;
                font-weight: bold;
                background-color: #212121;
            }
        """)

        self.detail_company = QLabel("Company: -")
        self.detail_position = QLabel("Position: -")
        self.detail_location = QLabel("Location: -")
        self.detail_status = QLabel("Status: -")

        self.detail_notes = QTextEdit()
        self.detail_notes.setReadOnly(True)
        self.detail_notes.setMinimumHeight(120)

        self.open_resume_button = QPushButton("Open Resume")
        self.open_resume_button.setEnabled(False)
        self.open_cover_button = QPushButton("Open Cover Letter")
        self.open_cover_button.setEnabled(False)

        for btn in [self.open_resume_button, self.open_cover_button]:
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #2a2a2a;
                    color: #999;
                    border: 1px solid #444;
                    border-radius: 4px;
                    padding: 5px;
                }
                QPushButton:enabled {
                    background-color: #1e88e5;
                    color: white;
                }
                QPushButton:hover:enabled {
                    background-color: #1565c0;
                }
            """)

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

        # === SUSUN DALAM RIGHT CONTAINER ===
        right_layout.addWidget(self.running_time_label)
        right_layout.addWidget(right_box)
        right_layout.addStretch()

        # Hilangkan addStretch(), gantikan dengan agar isi vertikal memenuhi tinggi
        right_layout.setStretch(0, 0)  # time label
        right_layout.setStretch(1, 1)  # right_box isi penuh vertikal

        right_container.setLayout(right_layout)
        right_container.setFixedWidth(340)

        # === GABUNG KE LAYOUT UTAMA ===
        home_main_layout.addLayout(left_layout)
        home_main_layout.addWidget(right_container)
        home_main_layout.setStretch(0, 2)  # kiri fleksibel
        home_main_layout.setStretch(1, 0)  # kanan tetap

        # === PAGE 2: Statistics ===
        self.stats_page = QWidget()
        stats_layout = QVBoxLayout(self.stats_page)
        stats_label = QLabel("Statistics Page — coming soon...")
        stats_label.setAlignment(Qt.AlignCenter)
        stats_label.setStyleSheet("font-size: 14px; color: #555;")
        stats_layout.addWidget(stats_label)

        # === PAGE 3: Reminders ===
        self.reminders_page = QWidget()
        reminders_layout = QVBoxLayout(self.reminders_page)
        reminders_label = QLabel("Reminders Page — coming soon...")
        reminders_label.setAlignment(Qt.AlignCenter)
        reminders_label.setStyleSheet("font-size: 14px; color: #555;")
        reminders_layout.addWidget(reminders_label)

        # === PAGE 4: Contacts ===
        self.contact_page = QWidget()
        contact_layout = QVBoxLayout(self.contact_page)

        contact_label = QLabel("Contact Page — coming soon...")
        contact_label.setAlignment(Qt.AlignCenter)
        contact_label.setStyleSheet("font-size: 14px; color: #555;")

        contact_layout.addWidget(contact_label)


        # Tambahkan ke stacked widget
        self.pages.addWidget(self.home_page)
        self.pages.addWidget(self.stats_page)
        self.pages.addWidget(self.reminders_page)
        self.pages.addWidget(self.contact_page)

        # Gabungkan Side Menu + Pages
        main_layout.addWidget(self.side_menu)
        main_layout.addWidget(self.pages)

        # self.side_menu.setCurrentRow(0)




