from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QListWidget,
    QPushButton, QLabel, QTableWidget, QTableWidgetItem, QHeaderView,
    QMessageBox
)
from PySide6.QtCore import Qt
from app.add_dialog import AddDialog
from app.database import add_application, get_all_applications


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("apply_me! – Job Application Tracker")
        self.resize(1000, 600)
        self._setup_ui()
        self.load_data()  # langsung muat data saat start

    def open_add_dialog(self):
        """Buka form tambah data"""
        dialog = AddDialog(self)
        if dialog.exec():
            data = dialog.get_data()
            add_application(**data)
            QMessageBox.information(self, "Success", "Application saved successfully!")
            self.load_data()

    def _setup_ui(self):
        """Bangun tampilan utama"""
        main_widget = QWidget()
        main_layout = QHBoxLayout(main_widget)

        # === Sidebar ===
        self.sidebar = QListWidget()
        self.sidebar.addItems(["🏠 Dashboard", "📂 Applications", "📊 Statistics", "⚙️ Settings"])
        self.sidebar.setFixedWidth(200)
        self.sidebar.setStyleSheet("""
            QListWidget {
                background-color: #1E1E1E;
                color: white;
                border: none;
                font-size: 13pt;
                padding: 8px;
            }
            QListWidget::item:selected {
                background-color: #0078D7;
                border-radius: 4px;
            }
        """)

        # === Dashboard Area ===
        self.dashboard = QWidget()
        dash_layout = QVBoxLayout(self.dashboard)

        title = QLabel("My Job Applications")
        title.setStyleSheet("font-size: 20px; font-weight: bold; margin-bottom: 8px;")
        dash_layout.addWidget(title)

        # === Table ===
        self.table = QTableWidget(0, 5)
        self.table.setHorizontalHeaderLabels(["Company", "Position", "Date Applied", "Status", "Source"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        dash_layout.addWidget(self.table)

        # === Add Button ===
        self.btn_add = QPushButton("＋ Add Application")
        self.btn_add.setFixedWidth(180)
        self.btn_add.clicked.connect(self.open_add_dialog)
        dash_layout.addWidget(self.btn_add, alignment=Qt.AlignRight)

        # === Styling ===
        self.setStyleSheet("""
            QMainWindow {
                background-color: #121212;
                color: white;
                font-family: 'Segoe UI';
            }
            QPushButton {
                background-color: #0078D7;
                color: white;
                border-radius: 6px;
                padding: 8px 14px;
                font-weight: 500;
            }
            QPushButton:hover {
                background-color: #0A84FF;
            }
            QHeaderView::section {
                background-color: #0078D7;
                color: white;
                border: none;
                padding: 6px;
            }
            QTableWidget {
                background-color: #1E1E1E;
                color: white;
                border: none;
                gridline-color: #333;
                font-size: 10.5pt;
            }
            QTableWidget::item:selected {
                background-color: #0A84FF;
            }
        """)

        # === Gabungkan layout utama ===
        main_layout.addWidget(self.sidebar)
        main_layout.addWidget(self.dashboard)
        self.setCentralWidget(main_widget)

    def load_data(self):
        """Muat data dari database (urut DESC — terbaru di atas)"""
        rows = get_all_applications()  # ambil data dari DB

        # urutkan dari ID terbesar ke terkecil (DESC)
        rows.sort(key=lambda x: x[0], reverse=True)

        self.table.setRowCount(len(rows))
        for i, row in enumerate(rows):
            # row: (id, company, position, location, date, source, status, ...)
            self.table.setItem(i, 0, QTableWidgetItem(row[1]))  # Company
            self.table.setItem(i, 1, QTableWidgetItem(row[2]))  # Position
            self.table.setItem(i, 2, QTableWidgetItem(row[4]))  # Date Applied
            self.table.setItem(i, 3, QTableWidgetItem(row[6]))  # Status
            self.table.setItem(i, 4, QTableWidgetItem(row[5]))  # Source
