from PySide2.QtCore import Qt
from PySide2.QtWidgets import QApplication, QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, \
    QSpacerItem
import sys
import re
import requests
import app_login


class RegistrationWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Registration")
        self.setMinimumSize(350, 500)
        self.setMaximumSize(350, 500)

        layout = QVBoxLayout()
        layout.setSpacing(10)  # Set a smaller spacing value
        layout.setAlignment(Qt.AlignCenter)  # Align the layout to the center horizontally

        # Add a spacer item for the top margin
        top_spacer = QSpacerItem(20, 20)
        layout.addItem(top_spacer)

        first_name_label = QLabel("First Name:")
        self.first_name_field = QLineEdit()
        self.first_name_field.setFixedWidth(250)
        layout.addWidget(first_name_label)
        layout.addWidget(self.first_name_field)

        last_name_label = QLabel("Last Name:")
        self.last_name_field = QLineEdit()
        self.last_name_field.setFixedWidth(250)
        layout.addWidget(last_name_label)
        layout.addWidget(self.last_name_field)

        email_label = QLabel("Email:")
        self.email_field = QLineEdit()
        self.email_field.setFixedWidth(250)
        layout.addWidget(email_label)
        layout.addWidget(self.email_field)

        password_label = QLabel("Password:")
        self.password_field = QLineEdit()
        self.password_field.setFixedWidth(250)
        self.password_field.setEchoMode(QLineEdit.Password)
        layout.addWidget(password_label)
        layout.addWidget(self.password_field)

        user_type_label = QLabel("User Type:")
        self.user_type_field = QLineEdit()
        self.user_type_field.setFixedWidth(250)
        layout.addWidget(user_type_label)
        layout.addWidget(self.user_type_field)

        created_by_label = QLabel("Created By:")
        self.created_by_field = QLineEdit()
        self.created_by_field.setFixedWidth(250)
        layout.addWidget(created_by_label)
        layout.addWidget(self.created_by_field)

        spacer_item = QSpacerItem(20, 20)
        layout.addItem(spacer_item)

        register_button = QPushButton("Register")
        register_button.clicked.connect(self.register)
        layout.addWidget(register_button, alignment=Qt.AlignCenter)

        self.setLayout(layout)

    def register(self):
        first_name = self.first_name_field.text()
        last_name = self.last_name_field.text()
        email = self.email_field.text()
        password = self.password_field.text()
        user_type = self.user_type_field.text()
        created_by = self.created_by_field.text()

        if not self.validate_email(email):
            QMessageBox.warning(self, "Invalid Email", "Please enter a valid email address.")
            return

        if not all([first_name, last_name, email, password]):
            QMessageBox.warning(self, "Missing Fields", "Please fill in all the required fields.")
            return

        if len(password) < 5:
            QMessageBox.warning(self, "Weak Password", "Password should be at least 5 characters long.")
            return

        payload = {
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "password": password,
            "user_type": int(user_type),
            "created_by": int(created_by) if created_by else None
        }

        try:
            response = requests.post("http://0.0.0.0:8000/user/create_user/", json=payload)
            response.raise_for_status()  # Raise an exception for any HTTP errors
            json_response = response.json()

            # Get user token and user type from the response
            user_token = json_response.get("access_token")
            user_type = json_response.get("user_type")

            print("User created successfully:")
            print("User Token:", user_token)
            print("User Type:", user_type)

            QMessageBox.information(self, "Registration Successful", "User created successfully.")
            self.close()
        except requests.exceptions.RequestException as e:
            QMessageBox.warning(self, "Registration Failed", str(e))

    def validate_email(self, email):
        # Simple email validation using regular expression
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        return re.match(pattern, email) is not None

    def closeEvent(self, event):
        reply = QMessageBox.question(self, "Confirm Exit", "Are you sure you want to exit?",
                                     QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            app.quit()
        else:
            event.ignore()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    registration_window = RegistrationWindow()
    registration_window.show()

    if registration_window.exec_() == QDialog.Accepted:
        print("Login successful")
        main_window = app_login.LoginWindow()
    else:
        sys.exit(0)  # Quit the program if login is canceled

    sys.exit(app.exec_())
