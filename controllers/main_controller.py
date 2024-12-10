from PyQt6.QtWidgets import QApplication
from ui.auth_window import AuthWindow
from ui.register_window import RegisterWindow
from ui.main_window import MainWindow
from logic.business_logic import BusinessLogic
from logic.network_layer import NetworkLayer
import sys


class MainController:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.network_layer = NetworkLayer() 
        self.business_logic = BusinessLogic(self.network_layer)
        self.auth_window = AuthWindow(self)
        self.register_window = RegisterWindow(self.business_logic, self)
        self.main_window = MainWindow(self.business_logic)


    def show_auth_window(self):
        self.register_window.hide()
        self.auth_window.show()

    def show_register_window(self):
        self.auth_window.hide()
        self.register_window.show()

    def show_main_window(self):
        self.auth_window.hide()
        self.main_window.show()

    def run(self):
        self.show_auth_window()
        sys.exit(self.app.exec())
