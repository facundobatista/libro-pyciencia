import csv
import pathlib
import string
import sys
import textwrap
import threading
import time
import traceback
from functools import partial

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg, NavigationToolbar2QT
from PyQt6.QtCore import QAbstractTableModel, QObject, Qt, pyqtSignal
from PyQt6.QtGui import QIcon, QAction, QMovie
from PyQt6.QtWidgets import (
    QApplication,
    QFileDialog,
    QHeaderView,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QMessageBox,
    QPlainTextEdit,
    QRadioButton,
    QStatusBar,
    QTableView,
    QToolBar,
    QVBoxLayout,
    QWidget,
)
from scipy.optimize import curve_fit

# backend no interactivo, para que no nos traiga problemas generar el
# gráfico en otro hilo; luego a la figura la asociamos nosotros con Qt
matplotlib.use("Agg")

# funciones para ajustar los datos; lineal, cuadrática y cúbica
functions_to_fit = {
    1: lambda x, a, b: a * x + b,
    2: lambda x, a, b, c: a * x**2 + b * x + c,
    3: lambda x, a, b, c, d: a * x**3 + b * x**2 + c * x + d,
}


def fit(data, degree):
    """Ajusta los datos con una función según el grado especificado."""
    try:
        fit_function = functions_to_fit[degree]
    except KeyError:
        raise ValueError(f"No hay una función para el grado requerido: {degree!r}")

    # los datos fuentes es una tabla de dos columnas, x e y; necesitamos esas dos columnas
    # por separado como entrada a la función de ajuste
    x_data, y_data = (np.array(x) for x in zip(*data))

    params, pcovs = curve_fit(fit_function, x_data, y_data)

    param_texts = []
    for idx, (pvalue, pname) in enumerate(zip(params, string.ascii_lowercase)):
        pcov = pcovs[idx, idx]
        param_texts.append(f"{pname} = {pvalue:.3f} ± {pcov:.3f}")

    fig = plt.figure()
    ax = fig.subplots()
    ax.plot(x_data, y_data, '.')
    ax.plot(x_data, fit_function(x_data, *params))
    ax.set_xlabel("x")
    ax.set_ylabel("y")

    # simulamos que la tarea tarda mucho tiempo, y es bloqueante, así mostramos cómo
    # lidiar con esta situación a nivel GUI
    time.sleep(5)

    return param_texts, fig


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


class TaskSignals(QObject):
    """Señales para conectar de nuestra ThreadedTask."""
    success = pyqtSignal(object)
    error = pyqtSignal(Exception)


class ThreadedTask(threading.Thread):
    """Ejecuta una función en un hilo.

    Recibe la función y los argumentos. En 'signals' provee 'success' para cuando la función
    se completa satisfactoriamente (envía el resultado) y 'error' para cuando no (envía
    la excepción).
    """
    def __init__(self, func, *args, **kwargs):
        self.func = func
        self.args = args
        self.kwargs = kwargs
        self.signals = TaskSignals()
        super().__init__()

    def run(self):
        try:
            result = self.func(*self.args, **self.kwargs)
        except Exception as exc:
            self.signals.error.emit(exc)
        else:
            self.signals.success.emit(result)


class ResultPanel(QWidget):
    """Panel para mostrar el resultado: parámetros y el gráfico en sí."""
    def __init__(self, parent, fit_parameters, matplotlib_figure):
        super().__init__()
        self.parent = parent
        layout = QVBoxLayout()
        self.setLayout(layout)

        # los parámetros de la ecuación
        params_textedit = QPlainTextEdit()
        params_textedit.setPlainText("\n".join(fit_parameters))
        layout.addWidget(params_textedit)

        # el gráfico, y su toolbar relacionado que lo agregamos a la ventana principal
        figure_canvas = FigureCanvasQTAgg(matplotlib_figure)
        layout.addWidget(figure_canvas)
        self.toolbar = NavigationToolbar2QT(figure_canvas, self)
        self.parent.main_window.addToolBar(self.toolbar)

    def close(self):
        """Remueve la toolbar antes de cerrar el widget."""
        self.parent.main_window.removeToolBar(self.toolbar)
        super().close()


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
            radio.clicked.connect(partial(self.calculate, degree))
            options.addWidget(radio)

        # throbber y resultados para alternar en la parte derecha
        self.throbber = None
        self.result_panel = None

    def calculate(self, function_degree):
        """Pone a realizar los cálculos en un hilo."""
        self.main_window.set_status("Calculando")

        self.throbber = QLabel()
        movie = QMovie("throbber.gif")
        self.throbber.setMovie(movie)
        movie.start()

        if self.result_panel is None:
            # primera vez, no hay resultados de antes, sólo agregamos el throbber
            self.right_layout.addWidget(self.throbber, stretch=1)
        else:
            # reemplazamos los resultados previos con el throbber
            self.right_layout.replaceWidget(self.result_panel, self.throbber)
            self.result_panel.close()

        # disparamos el nuevo cálculo y conectamos la función que muestra el resultado
        tt = ThreadedTask(fit, self.data, function_degree)
        tt.signals.success.connect(self.show_result)
        tt.signals.error.connect(self.on_error)
        tt.start()

    def on_error(self, exc):
        """Muestra el error que sucedió al hacer el cálculo."""
        # un resumen del problema en la interfaz
        self.main_window.show_error(f"Error al calcular! {exc!r}")
        # y el traceback completo por la terminal
        print("ERROR al calcular:")
        traceback.print_exception(exc)
        # deja el panel en un estado sano
        self.right_layout.removeWidget(self.throbber)
        self.throbber.close()

    def show_result(self, result):
        """Arma el panel con el resultado y reemplaza al throbber."""
        self.main_window.set_status("Mostrando el resultado")
        fit_parameters, matplotlib_figure = result
        self.result_panel = ResultPanel(self, fit_parameters, matplotlib_figure)
        self.right_layout.replaceWidget(self.throbber, self.result_panel)
        self.throbber.close()

    def close(self):
        """Remueve la toolbar antes de cerrar el widget."""
        if self.result_panel is not None:
            self.result_panel.close()
        super().close()


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
        title = "Python para Ciencia y Tecnología"
        text = textwrap.dedent("""
            Ejemplo de aplicación gráfica para el libro
            Python para Ciencia y Tecnología
            de Facundo Batista y Manuel Carlevaro

            http://pyciencia.taniquetil.com.ar/
        """)
        QMessageBox.about(self, title, text)


app = QApplication(sys.argv)
window = Window()
window.show()
sys.exit(app.exec())

# Copyright 2020-2025 Facundo Batista y Manuel Carlevaro
# Licencia CC BY-NC-SA 4.0
# Para más info visitar https://github.com/facundobatista/libro-pyciencia/
