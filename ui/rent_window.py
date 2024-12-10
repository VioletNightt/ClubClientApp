from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton
from datetime import datetime, timedelta
from ui.rent_dialog import RentDialog


def calculate_remaining_time(rental_end_time):
    """Вычисляет оставшееся время аренды."""
    end_time = datetime.strptime(rental_end_time, "%Y-%m-%dT%H:%M:%S.%f")
    remaining_time = end_time - datetime.now()
    if remaining_time.total_seconds() > 0:
        return remaining_time
    else:
        return timedelta(seconds=0)


def format_remaining_time(remaining_time):
    """Форматирует оставшееся время аренды для отображения."""
    minutes, seconds = divmod(remaining_time.total_seconds(), 60)
    return f"{int(minutes)} мин {int(seconds)} сек"


class RentComputerWidget(QWidget):
    def __init__(self, business_logic):
        super().__init__()
        self.business_logic = business_logic
        self.setLayout(QVBoxLayout())

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["ID", "Название", "Конфигурация", "Действие"])
        self.layout().addWidget(self.table)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_rental_timers)

        self.rental_timers = {}

    def showEvent(self, event):
        """Событие, вызываемое при отображении виджета."""
        super().showEvent(event)
        self.load_computers()
        self.timer.start(1000)

    def hideEvent(self, event):
        """Событие, вызываемое при скрытии виджета."""
        super().hideEvent(event)
        self.timer.stop()

    def load_computers(self):
        """Загружает список доступных компьютеров через BusinessLogic и обновляет таблицу."""
        try:
            computers = self.business_logic.get_available_computers()
            self.populate_table(computers)
        except Exception as e:
            print(f"Ошибка загрузки компьютеров: {e}")

    def populate_table(self, computers):
        """Обновляет таблицу компьютеров."""
        self.table.setRowCount(len(computers))

        for row, computer in enumerate(computers):
            self.table.setItem(row, 0, QTableWidgetItem(str(computer["id"])))
            self.table.setItem(row, 1, QTableWidgetItem(computer["name"]))
            self.table.setItem(row, 2, QTableWidgetItem(computer["configuration"]))

            if self.table.cellWidget(row, 3):
                self.table.removeCellWidget(row, 3)

            if computer["status"] == "rented" and computer["rental_end_time"]:
                remaining_time = calculate_remaining_time(computer["rental_end_time"])
                if remaining_time.total_seconds() > 0:
                    countdown_label = QTableWidgetItem(format_remaining_time(remaining_time))
                    self.table.setItem(row, 3, countdown_label)
                    self.rental_timers[computer["id"]] = datetime.strptime(
                        computer["rental_end_time"], "%Y-%m-%dT%H:%M:%S.%f"
                    )
                else:
                    self.table.setItem(row, 3, QTableWidgetItem("Аренда завершена"))
            else:
                rent_button = QPushButton("Арендовать")
                rent_button.clicked.connect(lambda _, c_id=computer["id"]: self.open_rent_dialog(c_id))
                self.table.setCellWidget(row, 3, rent_button)

        self.table.resizeColumnsToContents()

    def update_rental_timers(self):
        """Обновляет таймеры для арендованных компьютеров."""
        for row in range(self.table.rowCount()):
            item = self.table.item(row, 0) 
            if item is None:
                continue
            computer_id = int(item.text())
            if computer_id in self.rental_timers:
                remaining_time = self.rental_timers[computer_id] - datetime.now()
                if remaining_time.total_seconds() > 0:
                    self.table.item(row, 3).setText(format_remaining_time(remaining_time))
                else:
                    self.table.item(row, 3).setText("Аренда завершена")
                    del self.rental_timers[computer_id]

    def open_rent_dialog(self, computer_id):
        """Открывает диалоговое окно для аренды компьютера."""
        dialog = RentDialog(computer_id)
        if dialog.exec():
            duration = dialog.get_duration()
            try:
                self.business_logic.rent_computer(
                    computer_id=computer_id,
                    duration=duration["value"],
                    unit=duration["unit"]
                )
                if duration["unit"] == "minutes":
                    rental_duration = timedelta(minutes=duration["value"])
                elif duration["unit"] == "hours":
                    rental_duration = timedelta(hours=duration["value"])
                else:
                    raise ValueError("Неподдерживаемая единица измерения времени")

                rental_end_time = datetime.now() + rental_duration
                self.rental_timers[computer_id] = rental_end_time

                self.load_computers()
            except Exception as e:
                print(f"Ошибка при аренде компьютера: {e}")
