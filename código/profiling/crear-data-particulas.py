"""Genera data fuente para el ejemplo de contar partículas.

En cada archivo se grabaran varias lineas con la posición de la partícula dentro de
una caja de medición dada y su tamaño, todos valores al azar.
"""

import argparse
import pathlib
import random
import uuid

Q_FILES = 16_000
Q_PARTICLES = 10_000
MEASUREMENT_SIDE_LENGTH = 5_000
MAX_PARTICLE_SIZE = 500


def create_file(filepath):
    """Create an example file."""
    with filepath.open("xt") as fh:
        for _ in range(Q_PARTICLES):
            x = random.random() * MEASUREMENT_SIDE_LENGTH
            y = random.random() * MEASUREMENT_SIDE_LENGTH
            size = random.random() * MAX_PARTICLE_SIZE
            fh.write(f"{x},{y},{size}\n")


def main(basedir):
    """Punto de entrada principal."""
    if not basedir.exists():
        basedir.mkdir()

    for _ in range(Q_FILES):
        fname = uuid.uuid4().hex
        dirpath = basedir / fname[0] / fname[1]
        dirpath.mkdir(exist_ok=True, parents=True)
        create_file(dirpath / fname)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "dirpath", type=pathlib.Path, help="El directorio donde crear los ejemplos")
    args = parser.parse_args()
    if args.dirpath.exists() and list(args.dirpath.iterdir()):
        print("Error: el directorio indicado ya existe y tiene contenido.")
        exit(1)
    main(args.dirpath)

# Copyright 2020-2025 Facundo Batista y Manuel Carlevaro
# Licencia CC BY-NC-SA 4.0
# Para más info visitar https://github.com/facundobatista/libro-pyciencia/
