import sys

from PyQt6.QtWidgets import QApplication, QWidget
from PyQt6.QtGui import QIcon


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(250, 150)
        self.setWindowTitle("Primer ejemplo")
        self.setWindowIcon(QIcon("icon.png"))


app = QApplication(sys.argv)
window = Window()
window.show()
sys.exit(app.exec())

# Copyright 2020-2024 Facundo Batista y Manuel Carlevaro
# Licencia CC BY-NC-SA 4.0
# Para más info visitar https://github.com/facundobatista/libro-pyciencia/
