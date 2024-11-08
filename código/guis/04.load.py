import csv
import pathlib
import sys

from PyQt6.QtGui import QIcon, QAction
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QApplication,
    QFileDialog,
    QLabel,
    QMainWindow,
    QStatusBar,
    QToolBar,
)


class Window(QMainWindow):
    """Ventana principal."""

    def __init__(self):
        super().__init__()
        self.resize(400, 300)
        self.setWindowTitle("Ejemplo de interfaz gráfica")
        self.setWindowIcon(QIcon("icon.png"))

        # menú y barra de herramientas
        toolbar = QToolBar("main-toolbar")
        self.addToolBar(toolbar)
        self._status_bar = QStatusBar(self)
        self.setStatusBar(self._status_bar)
        menubar = self.menuBar()

        # las diferentes acciones tanto para el menu como para la barra de herramientas
        open_action = QAction(QIcon.fromTheme("document-open"), "Abrir archivo", self)
        open_action.setToolTip("Abrir archivo de datos")
        open_action.triggered.connect(self.on_open)
        open_action.setShortcut('Ctrl+A')
        quit_action = QAction(QIcon(), "Salir", self)
        quit_action.triggered.connect(app.exit)
        about_action = QAction(QIcon(), "Acerca de...", self)
        about_action.triggered.connect(self.on_about)

        # configuramos la barra de herramientas
        toolbar.addAction(open_action)

        # configuramos el menú
        menu = menubar.addMenu("&Archivo")
        menu.addAction(open_action)
        menu.addAction(quit_action)
        menu = menubar.addMenu("A&yuda")
        menu.addAction(about_action)

        self._status_bar.showMessage("Comenzando", 3000)

        label = QLabel("Python en Ámbitos Científicos")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setCentralWidget(label)

    def on_open(self):
        """Abre un nuevo archivo de datos y refresca el widget principal."""
        self._status_bar.showMessage("Abriendo archivo con datos", 3000)

        # abrimos un diálogo para que se seleccione un archivo
        filepath, filters = QFileDialog.getOpenFileName(self, "Abrir archivo")
        if not filepath:
            self._status_bar.showMessage("Ningún archivo seleccionado", 3000)
            return
        filepath = pathlib.Path(filepath)

        # abrimos el archivo y levantamos los datos
        try:
            with open(filepath) as csvfile:
                reader = csv.reader(csvfile)
                raw_data = list(reader)
        except Exception as exc:
            self._status_bar.showMessage(f"No se pudo abrir el archivo correctamente: {exc}", 3000)
            return

        # convertimos los datos a punto flotante, validando largos y descartando las listas vacias
        data = []
        for idx, row in enumerate(raw_data, 1):
            if not row:
                continue
            if len(row) != 2:
                self._status_bar.showMessage(
                    f"La linea {idx} del archivo no tiene exactamente dos columnas", 3000)
                return
            try:
                converted = [float(datum) for datum in row]
            except ValueError:
                self._status_bar.showMessage(
                    f"La linea {idx} del archivo tiene datos inválidos", 3000)
                return
            data.append(converted)

        # tenemos los datos ok!
        self._status_bar.showMessage("Archivo abierto correctamente", 3000)

        label = QLabel(f"Registros cargados: {len(data)}")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setCentralWidget(label)

    def on_about(self):
        pass


app = QApplication(sys.argv)
window = Window()
window.show()
sys.exit(app.exec())

# Copyright 2020-2024 Facundo Batista y Manuel Carlevaro
# Licencia CC BY-NC-SA 4.0
# Para más info visitar https://github.com/facundobatista/libro-pyciencia/
