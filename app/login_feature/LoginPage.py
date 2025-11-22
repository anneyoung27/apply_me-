from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel,
    QLineEdit, QHBoxLayout, QPushButton
)
from PySide6.QtGui import QPixmap, QIcon
from PySide6.QtCore import Qt, QSize
import os
import sys

# Class QLabel klik-able
class ClickableImage(QLabel):
    def __init__(self, icon_path, icon_path_alt, callback=None):
        super().__init__()
        self.icon1 = QPixmap(icon_path)
        self.icon2 = QPixmap(icon_path_alt)
        self.setPixmap(self.icon1)
        self.setFixedSize(self.icon1.size())
        self.toggled = False
        self.callback = callback  # fungsi tambahan saat klik

    def mousePressEvent(self, event):
        self.toggled = not self.toggled
        if self.toggled:
            self.setPixmap(self.icon2)
        else:
            self.setPixmap(self.icon1)
        if self.callback:
            self.callback(self.toggled)

class LoginPage(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login Page")
        self.setWindowIcon(QIcon("assets/login_icon/apply-me-job-tracker-logo.png"))
        self.setFixedSize(400, 400)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        # Title
        title = QLabel("Log In")
        title.setStyleSheet("font-size: 24px; font-weight: bold;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        subtitle = QLabel("To track your job application")
        subtitle.setAlignment(Qt.AlignCenter)
        layout.addWidget(subtitle)

        # Username
        username_label = QLabel("Username")
        layout.addWidget(username_label)
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Enter your username")
        layout.addWidget(self.username_input)

        # Password
        password_label = QLabel("Password")
        layout.addWidget(password_label)

        pw_layout = QHBoxLayout()
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setPlaceholderText("Enter your password")
        pw_layout.addWidget(self.password_input)

        # Toggle password menggunakan ClickableImage
        base_dir = os.path.dirname(os.path.abspath(__file__))
        hide_icon = os.path.join(base_dir, "assets/login_icon/hide-password.png")
        unhide_icon = os.path.join(base_dir, "assets/login_icon/unhide-password.png")

        self.pw_toggle_img = ClickableImage(hide_icon, unhide_icon, callback=self.toggle_password)
        pw_layout.addWidget(self.pw_toggle_img)

        layout.addLayout(pw_layout)

        # Forgot password
        forgot_label = QLabel("<u><i>Forgot your password?</i></u>")
        forgot_label.setAlignment(Qt.AlignRight)
        layout.addWidget(forgot_label)

        # Login button
        login_btn = QPushButton("Log in ➤")
        login_btn.setStyleSheet("background-color: #007BFF; color: white; padding: 11px; font-size: 13px;")
        login_btn.setMinimumWidth(200)
        layout.addWidget(login_btn, alignment=Qt.AlignCenter)

        self.setLayout(layout)

    def toggle_password(self, toggled):
        if toggled:
            self.password_input.setEchoMode(QLineEdit.Normal)
        else:
            self.password_input.setEchoMode(QLineEdit.Password)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LoginPage()
    window.show()
    sys.exit(app.exec())
