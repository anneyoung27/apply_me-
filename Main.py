from PySide6.QtWidgets import QApplication
from app.MainWindow import MainWindow
from app.Database import init_db
import sys

if __name__ == "__main__":
    init_db()
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())