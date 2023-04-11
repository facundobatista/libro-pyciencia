import sys

from PyQt6.QtWidgets import QApplication, QVBoxLayout, QWidget, QLabel, QPushButton
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(250, 150)
        self.setWindowTitle("Primer ejemplo")
        self.setWindowIcon(QIcon("icon.png"))

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.message = "Python en Ámbitos Científicos"
        self.label = QLabel(self.message)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.label)

        button = QPushButton("Más felices")
        button.clicked.connect(self.happier)
        layout.addWidget(button)

    def happier(self):
        self.message += " :D"
        self.label.setText(self.message)


app = QApplication(sys.argv)
window = Window()
window.show()
sys.exit(app.exec())

# Copyright 2020-2023 Facundo Batista y Manuel Carlevaro
# Licencia CC BY-NC-SA 4.0
# Para más info visitar https://github.com/facundobatista/libro-pyciencia/
