from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QLabel, QLineEdit, 
                             QPushButton, QMessageBox)
from PyQt5.QtCore import Qt
from api_client import APIClient

class LoginWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login - Chemical Visualizer")
        self.setFixedSize(350, 250)
        self.setStyleSheet("background-color: #ffffff;")

        layout = QVBoxLayout()
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(15)

        # Title
        title = QLabel("Welcome Back")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 20px; font-weight: bold; color: #333;")
        layout.addWidget(title)

        # Inputs
        self.user_input = QLineEdit()
        self.user_input.setPlaceholderText("Username")
        self.user_input.setStyleSheet("padding: 8px; border: 1px solid #ccc; border-radius: 5px;")
        
        self.pass_input = QLineEdit()
        self.pass_input.setPlaceholderText("Password")
        self.pass_input.setEchoMode(QLineEdit.Password)
        self.pass_input.setStyleSheet("padding: 8px; border: 1px solid #ccc; border-radius: 5px;")

        layout.addWidget(self.user_input)
        layout.addWidget(self.pass_input)

        # Login Button
        btn_login = QPushButton("Sign In")
        btn_login.setCursor(Qt.PointingHandCursor)
        btn_login.setStyleSheet("""
            QPushButton {
                background-color: #1976D2; color: white; padding: 10px;
                border-radius: 5px; font-weight: bold;
            }
            QPushButton:hover { background-color: #1565C0; }
        """)
        btn_login.clicked.connect(self.handle_login)
        layout.addWidget(btn_login)

        self.setLayout(layout)

    def handle_login(self):
        username = self.user_input.text()
        password = self.pass_input.text()

        if not username or not password:
            QMessageBox.warning(self, "Error", "Fields cannot be empty")
            return

        # Call API
        data = APIClient.login(username, password)
        if data and 'token' in data:
            APIClient.set_token(data['token'])
            self.accept() # Close dialog with success result
        else:
            QMessageBox.critical(self, "Error", "Invalid Credentials")