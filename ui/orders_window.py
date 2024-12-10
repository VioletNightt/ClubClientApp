from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem


class OrdersWidget(QWidget):
    def __init__(self, business_logic):
        super().__init__()
        self.business_logic = business_logic

        self.setLayout(QVBoxLayout())

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["ID Заказа", "Статус", "Общая сумма", "Состав"])
        self.layout().addWidget(self.table)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.load_orders)


    def showEvent(self, event):
        """Событие, вызываемое при отображении виджета."""
        super().showEvent(event)
        self.load_orders()
        self.timer.start(10000)

    def hideEvent(self, event):
        """Событие, вызываемое при скрытии виджета."""
        super().hideEvent(event)
        self.timer.stop()

    def load_orders(self):
        """Загружает список заказов через BusinessLogic и обновляет таблицу."""
        try:
            orders = self.business_logic.get_user_orders()
            self.populate_table(orders)
        except Exception as e:
            print(f"Ошибка загрузки заказов: {e}")

    def populate_table(self, orders):
        """Заполняет таблицу заказов."""
        self.table.setRowCount(len(orders))
        for row, order in enumerate(orders):
            self.table.setItem(row, 0, QTableWidgetItem(str(order["id"])))
            self.table.setItem(row, 1, QTableWidgetItem(order["status"]))
            self.table.setItem(row, 2, QTableWidgetItem(f"{order['total_price']} руб."))

            items_description = "\n".join([
                f"{item['name']} - {item['quantity']} шт. ({item['price']} руб./шт.)"
                for item in order["items"]
            ])

            item_cell = QTableWidgetItem(items_description)
            item_cell.setTextAlignment(Qt.AlignmentFlag.AlignTop)
            self.table.setItem(row, 3, item_cell)

        self.table.resizeColumnsToContents()
        self.table.resizeRowsToContents()


