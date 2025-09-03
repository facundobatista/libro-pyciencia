from setuptools import Extension, setup

setup(
    ext_modules=[
        Extension(
            name="particulas_mod_7",
            sources=["particulas-mod.cpp"],
        ),
    ]
)

# Copyright 2020-2025 Facundo Batista y Manuel Carlevaro
# Licencia CC BY-NC-SA 4.0
# Para más info visitar https://github.com/facundobatista/libro-pyciencia/
