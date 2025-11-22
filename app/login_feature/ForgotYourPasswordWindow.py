from PySide6.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QSpacerItem, QSizePolicy
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QCursor, QIcon

from app.login_feature.ClickableLabel import ClickableLabel


class ForgotYourPasswordWindow(QWidget):
    def __init__(self, login_window=None):
        super().__init__()
        self.login_window = login_window
        self.setWindowIcon(QIcon("assets/others_icon/apply_me_job_tracker_logo.png"))
        self.setWindowTitle("Forgot Password")
        self.setFixedSize(400, 200)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignTop)
        layout.setSpacing(10)

        # Title
        title_label = QLabel("Forgot Your Password?")
        title_font = QFont()
        title_font.setPointSize(18)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)

        # "Remember your password? Login here" clickable
        self.login_here_label = ClickableLabel("Remember your password? <b>Login here</b>")
        self.login_here_label.setAlignment(Qt.AlignCenter)
        self.login_here_label.clicked.connect(self.go_to_login)
        layout.addWidget(self.login_here_label)

        layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Fixed))

        # Instruction
        instruction_label = QLabel("Enter your email or username to reset your password:")
        instruction_label.setAlignment(Qt.AlignLeft)
        layout.addWidget(instruction_label)

        # Email input
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Enter your email or username")
        layout.addWidget(self.email_input)

        # Reset password button
        self.reset_button = QPushButton("Reset Password")
        self.reset_button.setStyleSheet("""
            QPushButton {
                background-color: #007BFF;
                color: black;
                border-radius: 5px;
                padding: 8px;
            }
            QPushButton:pressed {
                background-color: #0056b3;
            }
        """)
        self.reset_button.setFixedWidth(200)
        self.reset_button.setCursor(QCursor(Qt.PointingHandCursor))
        layout.addWidget(self.reset_button, alignment=Qt.AlignCenter)


        self.setLayout(layout)

    def go_to_login(self):
        self.close()
        if self.login_window:
            self.login_window.show()
