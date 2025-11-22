from PySide6.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QSpacerItem, QSizePolicy
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QCursor, QIcon
from app.login_feature.ClickableLabel import ClickableLabel
import re
from app.database.Models import User
from datetime import datetime

class SignUpWindow(QWidget):
    def __init__(self, login_window=None, session=None):
        super().__init__()
        self.login_window = login_window
        self.session = session
        self.setWindowIcon(QIcon("assets/others_icon/apply_me_job_tracker_logo.png"))
        self.setWindowTitle("Sign Up")
        self.setFixedSize(400, 350)
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
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Name")
        layout.addWidget(self.name_input)

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

        # Error / info label
        self.info_label = QLabel("")
        self.info_label.setStyleSheet("color: red;")
        layout.addWidget(self.info_label)

        # Create Account Button
        self.create_button = QPushButton("Create Account")
        self.create_button.clicked.connect(self.validate_form)
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

        self.confirm_password_input.textChanged.connect(self.check_password_match) # check if password and confirm password same

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

    def validate_form(self):
        name = self.name_input.text()
        username = self.username_input.text()
        email = self.email_input.text()
        password = self.password_input.text()
        confirm = self.confirm_password_input.text()

        # Reset semua border ke default
        self.name_input.setStyleSheet("")
        self.username_input.setStyleSheet("")
        self.email_input.setStyleSheet("")
        self.password_input.setStyleSheet("")
        self.confirm_password_input.setStyleSheet("")

        empty_fields = []

        if not name.strip():
            empty_fields.append(self.name_input)
        if not username.strip():
            empty_fields.append(self.username_input)
        if not email.strip():
            empty_fields.append(self.email_input)
        if not password.strip():
            empty_fields.append(self.password_input)
        if not confirm.strip():
            empty_fields.append(self.confirm_password_input)

        if empty_fields:
            for field in empty_fields:
                field.setStyleSheet("border: 2px solid red;")
            self.info_label.setText("Please fill out all fields!")
            self.info_label.setStyleSheet("color: red;")
            return

        # Validate email
        if "@" not in email or "." not in email:
            self.info_label.setText("Invalid email address!")
            self.info_label.setStyleSheet("color: red;")
            return

        # Validate password: starts with uppercase, contains lowercase, contains number
        if not re.match(r'^[A-Z]', password):
            self.info_label.setText("Password must start with an uppercase letter!")
            self.info_label.setStyleSheet("color: red;")
            return
        if not re.search(r'[a-z]', password):
            self.info_label.setText("Password must contain at least one lowercase letter!")
            self.info_label.setStyleSheet("color: red;")
            return
        if not re.search(r'\d', password):
            self.info_label.setText("Password must contain at least one number!")
            self.info_label.setStyleSheet("color: red;")
            return

        # Password and confirm password must match
        if password != confirm:
            self.info_label.setText("Password and Confirm Password do not match!")
            self.info_label.setStyleSheet("color: red;")
            return

        # If all validations pass
        self.confirm_password_input.setStyleSheet("border: 2px solid green;")
        self.info_label.setText("Validation successful! Account is ready to be created.")
        self.info_label.setStyleSheet("color: green;")

        # SIGN UP PROCESS
        if self.session is None:
            print("SESSION IS NONE!")
            return

        # Cek apakah username/email sudah terdaftar
        existing_user = (
            self.session.query(User)
            .filter((User.user_name == username) | (User.email == email))
            .first()
        )

        if existing_user:
            self.info_label.setText("Username or Email already exists!")
            self.info_label.setStyleSheet("color: red;")
            return

        name = self.name_input.text().strip()
        username = self.username_input.text().strip()
        email = self.email_input.text().strip()
        password = self.password_input.text().strip()

        if not (name and username and email and password):
            print("ALL FIELDS REQUIRED")
            return

        # INSERT USER
        new_user = User(
            name=name,
            user_name=username,
            email=email,
            password=password,
            created_at=datetime.now()
        )

        self.session.add(new_user)
        self.session.commit()

        self.info_label.setText("Account created successfully!")
        self.info_label.setStyleSheet("color: green;")

        # Kembali ke login window
        self.close()
        if self.login_window:
            self.login_window.show()

    def check_password_match(self):
        password = self.password_input.text()
        confirm = self.confirm_password_input.text()
        if password == confirm and confirm != "":
            self.confirm_password_input.setStyleSheet("border: 2px solid green;")
        else:
            self.confirm_password_input.setStyleSheet("")