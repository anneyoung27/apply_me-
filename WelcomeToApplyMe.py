from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication
from app.MainWindow import MainWindow
from app.database.Database import init_db
import sys

if __name__ == "__main__":
    init_db()
    app = QApplication(sys.argv)
    window = MainWindow()
    window.setWindowIcon(QIcon("assets/login_icon/apply-me-job-tracker-logo.png"))
    window.show()
    sys.exit(app.exec())