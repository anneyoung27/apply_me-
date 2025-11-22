from PySide6.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QSpacerItem, QSizePolicy
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QCursor
from app.login_feature.ClickableLabel import ClickableLabel

class SignUpWindow(QWidget):
    def __init__(self, login_window=None):
        super().__init__()
        self.login_window = login_window
        self.setWindowTitle("Sign Up")
        self.setFixedSize(400, 300)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignTop)
        layout.setSpacing(10)

        # Title
        title_label = QLabel("SIGN UP")
        title_font = QFont()
        title_font.setPointSize(20)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)

        layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Fixed))

        # Name
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Name")
        layout.addWidget(self.username_input)

        # Username
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username")
        layout.addWidget(self.username_input)

        # Email
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Email")
        layout.addWidget(self.email_input)

        # Password
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_input)

        # Confirm Password
        self.confirm_password_input = QLineEdit()
        self.confirm_password_input.setPlaceholderText("Confirm Password")
        self.confirm_password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.confirm_password_input)

        # Create Account Button
        self.create_button = QPushButton("Create Account")
        self.create_button.setStyleSheet("""
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
        self.create_button.setFixedWidth(200)
        self.create_button.setCursor(QCursor(Qt.PointingHandCursor))
        layout.addWidget(self.create_button, alignment=Qt.AlignCenter)

        # Already have account
        self.login_label = ClickableLabel("Already have an account? <b>Login here</b>")
        self.login_label.setAlignment(Qt.AlignCenter)
        self.login_label.clicked.connect(self.go_to_login)
        layout.addWidget(self.login_label)

        self.setLayout(layout)

    def go_to_login(self):
        self.close()
        if self.login_window:
            self.login_window.show()
