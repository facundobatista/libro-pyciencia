import csv
import pathlib
import sys
import textwrap

from PyQt6.QtGui import QIcon, QAction
from PyQt6.QtCore import QAbstractTableModel, Qt
from PyQt6.QtWidgets import (
    QApplication,
    QFileDialog,
    QHeaderView,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QMessageBox,
    QRadioButton,
    QStatusBar,
    QTableView,
    QToolBar,
    QVBoxLayout,
    QWidget,
)


class TableModel(QAbstractTableModel):
    """Modelo para la tabla de datos fuente."""

    def __init__(self, data):
        super(TableModel, self).__init__()
        self._src_data = data

    def headerData(self, section_index, orientation, role):
        """Devuelve información para armar los headers."""
        if orientation == Qt.Orientation.Horizontal and role == Qt.ItemDataRole.DisplayRole:
            return ["x", "y"][section_index]

    def data(self, index, role):
        """Devuelve información necesaria para mostrar los datos.

        - DisplayRole: el dato a mostrar
        - TextAlignmentRole: la alineación
        """
        if role == Qt.ItemDataRole.DisplayRole:
            # devolvemos el dato fuente según fila y columna, formateado lindo
            datum = self._src_data[index.row()][index.column()]
            return format(datum, ".5f")

        if role == Qt.ItemDataRole.TextAlignmentRole:
            # al centro en vertical, a la derecha en horizontal
            return Qt.AlignmentFlag.AlignVCenter + Qt.AlignmentFlag.AlignRight

    def rowCount(self, index):
        """Devuelve el total de filas."""
        return len(self._src_data)

    def columnCount(self, index):
        """Devuelve el total de columnas."""
        return len(self._src_data[0])


class MainPanel(QWidget):
    """Panel principal."""

    def __init__(self, main_window, filepath, data):
        super().__init__()
        self.main_window = main_window
        self.data = data

        # layout principal con dos layouts verticales a izquierda y derecha
        main_layout = QHBoxLayout()
        self.left_layout = QVBoxLayout()
        main_layout.addLayout(self.left_layout)
        self.right_layout = QVBoxLayout()
        self.right_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addLayout(self.right_layout, stretch=1)
        self.setLayout(main_layout)

        # la etiqueta con el nombre del archivo que estamos usando
        label = QLabel(filepath.name)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.left_layout.addWidget(label)

        # armamos una tabla, le asociamos un modelo, y configuramos su estética
        table = QTableView()
        table.setModel(TableModel(data))
        table.verticalHeader().setVisible(False)
        horizontal_header = table.horizontalHeader()
        horizontal_header.setStretchLastSection(True)
        horizontal_header.setSectionResizeMode(1, QHeaderView.ResizeMode.Interactive)
        self.left_layout.addWidget(table)

        # radiobuttons para la selección de qué función utilizar
        options = QVBoxLayout()
        self.left_layout.addLayout(options)
        for degree, name in enumerate(["Lineal", "Cuadrática", "Cúbica"], 1):
            radio = QRadioButton(name, self)
            options.addWidget(radio)


class Window(QMainWindow):
    """Ventana principal."""

    def __init__(self):
        super().__init__()
        self.resize(800, 600)
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

        self.main_panel = None
        self.set_status("Comenzando")

    def set_status(self, message):
        """Muestra un mensaje efímero en la barra de estado."""
        self._status_bar.showMessage(message, 3000)

    def show_error(self, message):
        """Muestra un mensaje de error via un diálogo y en la barra de estado."""
        self.set_status(f"Error: {message}")
        QMessageBox.critical(self, "Error", message)

    def on_open(self):
        """Abre un nuevo archivo de datos y refresca el widget principal."""
        self.set_status("Abriendo archivo con datos")

        # abrimos un diálogo para que se seleccione un archivo
        filepath, filters = QFileDialog.getOpenFileName(self, "Abrir archivo")
        if not filepath:
            self.set_status("Ningún archivo seleccionado")
            return
        filepath = pathlib.Path(filepath)

        # abrimos el archivo y levantamos los datos
        try:
            with open(filepath) as csvfile:
                reader = csv.reader(csvfile)
                raw_data = list(reader)
        except Exception as exc:
            self.show_error(f"No se pudo abrir el archivo correctamente: {exc}")
            return

        # convertimos los datos a punto flotante, validando largos y descartando las listas vacias
        data = []
        for idx, row in enumerate(raw_data, 1):
            if not row:
                continue
            if len(row) != 2:
                self.show_error(f"La linea {idx} del archivo no tiene exactamente dos columnas")
                return
            try:
                converted = [float(datum) for datum in row]
            except ValueError:
                self.show_error(f"La linea {idx} del archivo tiene datos inválidos")
                return
            data.append(converted)

        # tenemos los datos ok!
        self.set_status("Archivo abierto correctamente")

        # armamos el área principal dentro de la ventana
        if self.main_panel is not None:
            self.main_panel.close()
        self.main_panel = MainPanel(self, filepath, data)
        self.setCentralWidget(self.main_panel)

    def on_about(self):
        """Muestra el diálogo de Acerca de."""
        title = "Python en Ámbitos Científicos"
        text = textwrap.dedent("""
            Ejemplo de aplicación gráfica para el libro
            Python en Ámbitos Científicos
            de Facundo Batista y Manuel Carlevaro

            http://pyciencia.taniquetil.com.ar/
        """)
        QMessageBox.about(self, title, text)


app = QApplication(sys.argv)
window = Window()
window.show()
sys.exit(app.exec())

# Copyright 2020-2023 Facundo Batista y Manuel Carlevaro
# Licencia CC BY-NC-SA 4.0
# Para más info visitar https://github.com/facundobatista/libro-pyciencia/
