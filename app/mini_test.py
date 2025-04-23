from PySide6.QtWidgets import QApplication, QPushButton, QVBoxLayout, QWidget
from PySide6.QtCore import Qt

class MiniTest(QPushButton):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.default_color = "black"
        self.pressed_color = "red"

        # Set default text color
        self.setStyleSheet(f"color: {self.default_color};")

        # Connect the clicked signal to the color-changing slot
        self.clicked.connect(self.change_text_color)

    def change_text_color(self):
        # Check the current color and toggle it
        current_color = self.styleSheet()
        if self.pressed_color in current_color:
            self.setStyleSheet(f"color: {self.default_color};")
        else:
            self.setStyleSheet(f"color: {self.pressed_color};")