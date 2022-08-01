# Python en Ámbitos Científicos

[![Licencia](https://img.shields.io/badge/License-CC%20BY%20NC%20SA%204.0-blue.svg)](https://creativecommons.org/licenses/by-nc-sa/4.0/deed.es) [![Twitter](https://img.shields.io/twitter/follow/libro_pyciencia.svg?style=social)](https://twitter.com/libro_pyciencia)  

Este proyecto es parte del soporte de construcción del libro "Python en Ámbitos Científicos" de Facundo Batista y Manuel Carlevaro.

<img src="logo.png" width="200">

Todavía en desarrollo, aquí se irán publicando capítulos por separado (en distintos grados de finalización) con la idea de poder compartir el contenido y en lo posible ir recibiendo feedback.

Cada capítulo es un PDF diferente, y en el directorio `códigos`, bajo el directorio correspondiente a ese capítulo, estarán los programas en Python que se mencionan o usan en el texto.

Tanto los textos como el código fuente, ejemplos e imágenes son Copyright de Facundo Batista y Manuel Carlevaro y están compartidos bajo la licencia [Creative Commons Atribución-NoComercial-CompartirIgual 4.0 Internacional (CC BY-NC-SA 4.0)](https://creativecommons.org/licenses/by-nc-sa/4.0/deed.es), salvo que se especifique puntualmente lo contrario.


## Capítulos

- [Introducción a Python](intro.pdf?raw=True): Qué es Python. Propiedades del lenguaje, multiparadigma, interpretado. Biblioteca estándar, módulos externos, integrado en Python. Editando y ejecutando, usando módulos. El intérprete interactivo, Jupyter Notebooks, explorando. Tipos de datos: números, cadenas, listas, tuplas. Pensando como un Pythonista. Más tipos: conjuntos y diccionarios. Iteradores. Controles de flujo: if, while, for. Excepciones. Encapsulando código: funciones, espacios de nombres, generadores, clases, módulos. Cómo pedir ayuda.

- [Ecuaciones diferenciales ordinarias](ecuaciones_ordinarias.pdf?raw=True): Introducción. Solución analítica. Métodos numéricos. Ecuación diferencial con valores iniciales.

- [Numpy](numpy.pdf): Introducción y conceptos. El `array`. Multidimensionalidad. Slices. Indización avanzada, máscaras, arreglos correlacionados. Broadcasting.

- [Ecuaciones en derivadas parciales](ecuaciones_parciales.pdf?raw=True): Clasificación. Método de las diferencias finitas. Ecuación 1D con método explícito. Solución con método implícito. Implementación con matriz rala. Método de elementos finitos. Ecuación de Poisson. Formulación variacional. Implementación en FEniCS.

- [Aritmética de punto flotante](punto_flotante.pdf?raw=True): Introducción. La necesidad del punto flotante. La estructura y sus partes. Valores especiales.Binario y decimal. Errores, comparaciones. Uso en aplicaciones científicas.

- [Ecuaciones algebraicas](ecuaciones_algebraicas.pdf?raw=True): Sistemas de ecuaciones lineales. Condicionamiento. Factorización LU. Problema de autovalores. Ecuaciones no lineales de una y varias dimensiones.

- [Versionado de código](versionado.pdf?raw=True): Control de versiones, utilidad, necesidad, casos de uso. Ramas. Git. Flujo de traajo, ciclo de vida de una rama, ejemplo práctico. Lecturas recomendadas.

- [Integración numérica](integracion.pdf?raw=True): Integración simbólica. Transformaciones integrales. Integración numérica en una dimensión: métodos de Newton-Cotes, cuadraturas gaussianas, integración Monte Carlo. Integración numérica con SciPy. Integración múltiple. 

- [Entornos de ejecución de Python](entornos.pdf?raw=True): Introducción a la problemática. Descripción de la necesidad de múltiples entornos. Repetibilidad y aislamiento. Entornos virtuales, creación y activación, instalación de paquetes. Herramientas: virtualenv, virtualenvwrapper, fades, pipenv. Ejemplos prácticos. Contenedores, conceptos, distinción con imágenes. El Dockerfile. Creando imágenes. Ejecutando contenedores. Copiando resultados desde el contenedor. Valor de los contenedores a nivel sistema. Compartiendo imágenes.

- [Elementos de estadística](estadistica.pdf?raw=True): Números aleatorios. Distribuciones: medidas de centralidad y dispersión. Test de hipótesis. Estimación no paramétrica.

- [Procesamiento en paralelo](proc_paralelo.pdf?raw=True): Introducción. Qué es la concurrencia. Threading. Usando hilos. Modificando estructuras en sistemas multithreading, condiciones de carrera, locks. Sistemas asincrónicos, ventajas y desventajas. Usando async. Procesamiento en múltiples procesadores, compartiendo datos. Trabajando con números. Ejemplo práctico.

