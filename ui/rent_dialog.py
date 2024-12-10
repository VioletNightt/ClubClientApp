from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QSpinBox, QComboBox, QDialogButtonBox


class RentDialog(QDialog):
    def __init__(self, computer_id, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"Аренда компьютера #{computer_id}")
        self.setFixedSize(300, 140)

        self.computer_id = computer_id
        self.selected_duration = {"value": 1, "unit": "hours"}

        layout = QVBoxLayout(self)

        layout.addWidget(QLabel(f"Укажите время аренды для компьютера #{computer_id}:"))

        self.duration_input = QSpinBox()
        self.duration_input.setMinimum(1)
        self.duration_input.setMaximum(1000)
        self.duration_input.setValue(1)
        layout.addWidget(self.duration_input)

        self.unit_selector = QComboBox()
        self.unit_selector.addItems(["Минут", "Часов"])
        layout.addWidget(self.unit_selector)

        self.button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)
        layout.addWidget(self.button_box)

    def get_duration(self):
        """Возвращает выбранную длительность аренды."""
        unit = self.unit_selector.currentText()
        unit = "minutes" if unit == "Минут" else "hours"
        return {"value": self.duration_input.value(), "unit": unit}
