from PyQt6.QtWidgets import (
    QMainWindow, QListWidget, QStackedWidget, QHBoxLayout, QWidget
)

from ui.menu_window import RestaurantMenuWidget
from ui.orders_window import OrdersWidget
from ui.rent_window import RentComputerWidget


class MainWindow(QMainWindow):
    def __init__(self, business_logic):
        super().__init__()
        self.business_logic = business_logic
        self.setWindowTitle("Клиентское приложение")
        self.resize(1200, 800)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QHBoxLayout(central_widget)

        self.menu_list = QListWidget()
        self.content_stack = QStackedWidget()

        self.menu_list.addItem("Арендовать компьютер")
        self.menu_list.addItem("Меню ресторана")
        self.menu_list.addItem("Ваши заказы")
        self.menu_list.addItem("Выход")
        self.menu_list.setMaximumWidth(200)

        self.menu_list.currentRowChanged.connect(self.switch_view)

        self.rent_computer_widget = RentComputerWidget(self.business_logic)
        self.content_stack.addWidget(self.rent_computer_widget)

        self.restaurant_menu_widget = RestaurantMenuWidget(self.business_logic)
        self.content_stack.addWidget(self.restaurant_menu_widget)

        self.orders_widget = OrdersWidget(self.business_logic)
        self.content_stack.addWidget(self.orders_widget)

        layout.addWidget(self.menu_list)
        layout.addWidget(self.content_stack)

    def switch_view(self, index):
        if index == 3:
            self.close()
        else:
            self.content_stack.setCurrentIndex(index)
