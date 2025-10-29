from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QListWidget,
    QPushButton, QLabel, QTableWidget, QTableWidgetItem, QHeaderView,
    QFrame
)
from PySide6.QtCore import Qt
from app.add_dialog import AddDialog

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("apply_me! – Job Application Tracker")
        self.resize(1000, 600)
        self._setup_ui()

    def _setup_ui(self):
        main_widget = QWidget()
        main_layout = QHBoxLayout(main_widget)

        # === Sidebar ===
        self.sidebar = QListWidget()
        self.sidebar.addItems(["🏠 Dashboard", "📂 Applications", "📊 Statistics", "⚙️ Settings"])
        self.sidebar.setFixedWidth(200)
        self.sidebar.setStyleSheet("""
            QListWidget {
                background-color: #2C3E50;
                color: white;
                border: none;
                font-size: 23px;
            }
            QListWidget::item:selected {
                background-color: #3498DB;
            }
        """)

        # === Dashboard Area ===
        self.dashboard = QWidget()
        dash_layout = QVBoxLayout(self.dashboard)

        title = QLabel("My Job Applications")
        title.setStyleSheet("font-size: 20px; font-weight: bold;")
        dash_layout.addWidget(title)

        # Table
        self.table = QTableWidget(0, 4)
        self.table.setHorizontalHeaderLabels(["Company", "Position", "Date Applied", "Status"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        dash_layout.addWidget(self.table)

        # Add Button
        self.btn_add = QPushButton("＋ Add Application")
        self.btn_add.setFixedWidth(180)
        self.btn_add.clicked.connect(self.open_add_dialog)
        dash_layout.addWidget(self.btn_add, alignment=Qt.AlignRight)

        # Styling
        self.btn_add.setStyleSheet("""
            QPushButton {
                background-color: #27ae60;
                color: white;
                font-weight: bold;
                border-radius: 6px;
                padding: 8px 14px;
            }
            QPushButton:hover {
                background-color: #2ecc71;
            }
        """)

        # Combine layouts
        main_layout.addWidget(self.sidebar)
        main_layout.addWidget(self.dashboard)
        self.setCentralWidget(main_widget)

        # Dummy data
        self.add_table_row("Google", "Backend Engineer", "2025-10-29", "Applied")

    def add_table_row(self, company, position, date, status):
        row = self.table.rowCount()
        self.table.insertRow(row)
        self.table.setItem(row, 0, QTableWidgetItem(company))
        self.table.setItem(row, 1, QTableWidgetItem(position))
        self.table.setItem(row, 2, QTableWidgetItem(date))
        self.table.setItem(row, 3, QTableWidgetItem(status))

    def open_add_dialog(self):
        dialog = AddDialog(self)
        if dialog.exec():
            data = dialog.get_data()
            self.add_table_row(data["company"], data["position"], data["date"], data["status"])
