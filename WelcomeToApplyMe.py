from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication
from app.MainWindow import MainWindow
from app.database.Database import init_db
import sys

from app.login_feature.LoginWindow import LoginWindow

if __name__ == "__main__":
    init_db()
    app = QApplication(sys.argv)
    # window = MainWindow()
    window = LoginWindow()
    window.setWindowIcon(QIcon("assets/others_icon/apply_me_job_tracker_logo.png"))
    window.show()
    sys.exit(app.exec())