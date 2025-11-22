from PySide6.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout,
    QHBoxLayout, QCheckBox, QSpacerItem, QSizePolicy
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QCursor
from app.login_feature.SignUpWindow import SignUpWindow
from app.login_feature.ClickableLabel import ClickableLabel

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login Page")
        self.setFixedSize(400, 380)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignTop)
        layout.setSpacing(10)

        # Header
        title_label = QLabel("LOGIN")
        title_font = QFont()
        title_font.setPointSize(20)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignLeft)
        layout.addWidget(title_label)

        subtitle_label = QLabel("To track your job application")
        subtitle_font = QFont()
        subtitle_font.setPointSize(12)
        subtitle_label.setFont(subtitle_font)
        subtitle_label.setAlignment(Qt.AlignLeft)
        layout.addWidget(subtitle_label)

        layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Fixed))

        # Username
        layout.addWidget(QLabel("Username:"))
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Enter your username")
        layout.addWidget(self.username_input)

        # Password
        layout.addWidget(QLabel("Password:"))
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter your password")
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_input)

        # Remember + Forgot
        h_layout = QHBoxLayout()
        self.remember_checkbox = QCheckBox("Remember Me")
        h_layout.addWidget(self.remember_checkbox)

        self.forgot_label = QLabel('<u><i>Forgot your password?</i></u>')
        self.forgot_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        h_layout.addWidget(self.forgot_label, alignment=Qt.AlignRight)
        layout.addLayout(h_layout)

        # Login button
        layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Fixed))
        self.login_button = QPushButton("Log in")
        self.login_button.setStyleSheet("""
            QPushButton {
                background-color: #007BFF; 
                color: white; 
                border-radius: 5px; 
                padding: 8px;
            }
            QPushButton:pressed {
                background-color: #0056b3;
            }
        """)
        layout.addWidget(self.login_button)

        # Sign up label
        self.signup_label = ClickableLabel("Don't have an account? <b>Sign up now!</b>")
        self.signup_label.setAlignment(Qt.AlignCenter)
        self.signup_label.clicked.connect(self.open_signup_window)
        layout.addWidget(self.signup_label)

        self.setLayout(layout)

    def open_signup_window(self):
        self.signup_window = SignUpWindow(login_window=self)
        self.signup_window.show()
        self.hide()
