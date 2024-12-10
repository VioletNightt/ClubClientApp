from PyQt6.QtGui import QIntValidator
from PyQt6.QtWidgets import QVBoxLayout, QLabel, QLineEdit, QDialog, QDialogButtonBox

class QuantityDialog(QDialog):
    """Диалоговое окно для ввода количества порций."""
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Выберите количество")
        self.setFixedSize(200, 100)

        layout = QVBoxLayout()

        self.label = QLabel("Введите количество порций:")
        self.quantity_input = QLineEdit()
        self.quantity_input.setPlaceholderText("1")
        self.quantity_input.setValidator(QIntValidator(1, 1000))

        layout.addWidget(self.label)
        layout.addWidget(self.quantity_input)

        self.buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)

        layout.addWidget(self.buttons)
        self.setLayout(layout)

    def get_quantity(self):
        """Возвращает количество порций, если введено корректное значение."""
        return int(self.quantity_input.text()) if self.quantity_input.text().isdigit() else None
