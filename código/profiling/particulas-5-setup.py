from setuptools import setup
from Cython.Build import cythonize

setup(
    name="Ejemplo particulas",
    ext_modules=cythonize("particulas_mod_5.pyx", language_level="3", annotate=True),
)

# Copyright 2020-2024 Facundo Batista y Manuel Carlevaro
# Licencia CC BY-NC-SA 4.0
# Para más info visitar https://github.com/facundobatista/libro-pyciencia/
