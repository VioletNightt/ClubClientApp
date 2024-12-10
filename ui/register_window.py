from PyQt6.QtWidgets import QMainWindow, QLineEdit, QPushButton, QVBoxLayout, QWidget, QMessageBox


class RegisterWindow(QMainWindow):
    def __init__(self, business_logic, controller):
        super().__init__()
        self.business_logic = business_logic
        self.controller = controller
        self.setWindowTitle("Регистрация")
        self.setFixedSize(300, 250)

        self.login_field = QLineEdit(self)
        self.login_field.setPlaceholderText("Логин")

        self.email_field = QLineEdit(self)
        self.email_field.setPlaceholderText("Email")

        self.phone_field = QLineEdit(self)
        self.phone_field.setPlaceholderText("Телефон")

        self.password_field = QLineEdit(self)
        self.password_field.setPlaceholderText("Пароль")
        self.password_field.setEchoMode(QLineEdit.EchoMode.Password)

        self.register_button = QPushButton("Зарегистрироваться", self)
        self.cancel_button = QPushButton("Отмена", self)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.login_field)
        self.layout.addWidget(self.email_field)
        self.layout.addWidget(self.phone_field)
        self.layout.addWidget(self.password_field)
        self.layout.addWidget(self.register_button)
        self.layout.addWidget(self.cancel_button)

        container = QWidget()
        container.setLayout(self.layout)
        self.setCentralWidget(container)

        self.register_button.clicked.connect(self.handle_register)
        self.cancel_button.clicked.connect(self.controller.show_auth_window)

    def handle_register(self):
        """Обрабатывает регистрацию."""
        login = self.login_field.text()
        email = self.email_field.text()
        phone = self.phone_field.text()
        password = self.password_field.text()

        if not all([login, email, phone, password]):
            self.show_error("Заполните все поля")
            return

        try:
            result = self.business_logic.register_user(login, email, phone, password)
            print(result)
            if result["success"]:
                QMessageBox.information(self, "Успех", result["message"])
                self.controller.show_auth_window()
            else:
                self.show_error(result["error"])
        except Exception as e:
            self.show_error(f"Ошибка: {e}")

    def show_error(self, message):
        QMessageBox.warning(self, "Ошибка", message)
