from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton,
    QMessageBox, QLabel, QHBoxLayout, QInputDialog, QFrame
)
from PyQt6.QtCore import Qt


class RestaurantMenuWidget(QWidget):
    def __init__(self, business_logic):
        super().__init__()
        self.business_logic = business_logic
        self.orders = [] 

        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)

        self.menu_table = QTableWidget()
        self.menu_table.setColumnCount(3)
        self.menu_table.setHorizontalHeaderLabels(["Название", "Цена", "Действие"])
        self.main_layout.addWidget(self.menu_table)

        self.order_frame = QFrame()
        self.order_frame.setLayout(QVBoxLayout())
        self.order_frame.hide() 
        self.main_layout.addWidget(self.order_frame)

        self.order_label = QLabel("Ваш заказ:")
        self.order_frame.layout().addWidget(self.order_label)

        self.order_table = QTableWidget()
        self.order_table.setColumnCount(3)
        self.order_table.setHorizontalHeaderLabels(["Название", "Количество", "Цена"])
        self.order_frame.layout().addWidget(self.order_table)

        self.total_price_label = QLabel("Итоговая цена: 0 руб.")
        self.order_frame.layout().addWidget(self.total_price_label)

        self.submit_order_button = QPushButton("Отправить заказ")
        self.submit_order_button.clicked.connect(self.submit_order)
        self.order_frame.layout().addWidget(self.submit_order_button)

    def showEvent(self, event):
        """Загружает данные меню только при отображении виджета."""
        super().showEvent(event)
        self.load_menu()

    def load_menu(self):
        """Загружает данные меню из бизнес-логики."""
        try:
            menu_items = self.business_logic.get_menu_items()
            self.populate_menu_table(menu_items)
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка загрузки меню: {e}")

    def populate_menu_table(self, menu_items):
        """Заполняет таблицу меню."""
        self.menu_table.setRowCount(len(menu_items))
        for row, item in enumerate(menu_items):
            self.menu_table.setItem(row, 0, QTableWidgetItem(item["name"]))
            self.menu_table.setItem(row, 1, QTableWidgetItem(f"{item['price']} руб."))

            add_button = QPushButton("Добавить в заказ")
            add_button.clicked.connect(lambda _, i=item: self.add_to_order(i))
            self.menu_table.setCellWidget(row, 2, add_button)
        self.menu_table.resizeColumnsToContents()

    def add_to_order(self, item):
        """Добавляет блюдо в заказ."""
        quantity, ok = QInputDialog.getInt(self, "Количество", f"Введите количество для {item['name']}:",
                                           min=1, max=100, step=1)
        if ok:
            self.orders.append(
                {"item_id": item["id"], "quantity": quantity, "price": item["price"], "name": item["name"]})
            self.update_order_view()

    def update_order_view(self):
        """Обновляет отображение заказа."""
        if not self.order_frame.isVisible():
            self.order_frame.show()

        self.order_table.setRowCount(len(self.orders))
        total_price = 0
        for row, order in enumerate(self.orders):
            self.order_table.setItem(row, 0, QTableWidgetItem(order["name"]))
            self.order_table.setItem(row, 1, QTableWidgetItem(str(order["quantity"])))
            self.order_table.setItem(row, 2, QTableWidgetItem(f"{order['price'] * order['quantity']} руб."))
            total_price += order["price"] * order["quantity"]

        self.total_price_label.setText(f"Итоговая цена: {total_price} руб.")
        self.order_table.resizeColumnsToContents()

    def submit_order(self):
        """Отправляет заказ через бизнес-логику."""
        try:
            items = [{"item_id": order["item_id"], "quantity": order["quantity"]} for order in self.orders]
            self.business_logic.create_order(items)
            QMessageBox.information(self, "Успех", "Ваш заказ успешно оформлен!")
            self.orders.clear()
            self.update_order_view()
            self.order_frame.hide()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка отправки заказа: {e}")
