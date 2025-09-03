#!/usr/bin/env python3
"""Programa que resuelve la ecuación de calor en 1D."""

import argparse
from contextlib import contextmanager

import matplotlib.pyplot as plt
import matplotlib.cm as cmx
from matplotlib import colors
import numpy as np
from scipy import (
    linalg,  # Módulo de álgebra lineal, para el método implícito
    sparse,  # Paquete para matrices ralas
)
from scipy.sparse import linalg as sparse_linalg  # Solvers para matrices ralas

# Configure matplotlib
plt.rcParams.update({
    'text.usetex': True,
    'font.size': 14,
    'axes.labelsize': 'large',
})


def I(x):
    """Representa la curva de temperatura (en función de x) inicial (para t=0)

    Entonces u(x, 0) = I(x):
        u(0, 0) = 0
        u(1, 0) = 2
    """
    return 4 * x * (3 / 2 - x)


# Parámetros globales del problema
L = 1  # Longitud de la barra
T = 1  # Tiempo máximo de la solución
c = 2  # Difusividad térmica


@contextmanager
def graficar(x, t):
    """Muestra la temperatura en función de x y t."""

    # Semántica de tonos
    cm = plt.get_cmap('Greens_r')
    c_norm = colors.PowerNorm(gamma=0.25, vmin=t[0], vmax=t[-1])
    scalar_map = cmx.ScalarMappable(norm=c_norm, cmap=cm)

    # La curva en sí
    fig, ax = plt.subplots()

    def agregar_curva(point, u):
        cval = scalar_map.to_rgba(point)
        ax.plot(x, u, color=cval)

    # Pasamos la función para agregar las curvas
    yield agregar_curva

    # Dibujamos
    fig.colorbar(cmx.ScalarMappable(norm=c_norm, cmap=cm))
    plt.xlabel(r'$x$')
    plt.ylabel(r'$u(x)$')
    plt.show()


def resolver_explicito():
    """Método explícito."""
    # Puntos de resolución del problema
    Nx = 10  # Número de puntos de la malla en x
    Nt = 500  # Número de puntos de la malla en t
    h = L / Nx  # Paso en x
    k = T / Nt  # Paso en t
    F = c * k / h ** 2  # Número de malla de Fourier
    print(f'{h=} | {k=} | {F=}')

    # Malla en x y t
    x = np.linspace(0, L, Nx + 1)
    t = np.linspace(0, T, Nt + 1)

    # Valores de u(x,t)
    u = np.zeros(Nx + 1)  # u en j

    # Iteración en t (j)
    with graficar(x, t) as agregar_curva:
        # Condición inicial (y la dibujamos)
        up = I(x)
        agregar_curva(0, up)

        for j in range(1, Nt):
            # esténcil (sin los bordes)
            u[1:Nx] = up[1:Nx] + F * (up[0:Nx - 1] - 2 * up[1:Nx] + up[2:Nx + 1])

            # Condiciones de borde
            u[0] = 0
            u[Nx] = 2

            # Trazamos una solución cada 10 pasos en j
            if not j % 10:
                agregar_curva(j * k, u)

            # Cambiamos las variable antes del próximo paso
            up = u


def resolver_implicito():
    """Método implícito."""
    # Puntos de resolución del problema
    Nx = 100  # Número de puntos de la malla en x
    Nt = 1000  # Número de puntos de la malla en t
    h = L / Nx  # Paso en x
    k = T / Nt  # Paso en t
    F = c * k / h ** 2  # Número de malla de Fourier
    print(f'{h=} | {k=} | {F=}')

    # Malla en x y t
    x = np.linspace(0, L, Nx + 1)
    t = np.linspace(0, T, Nt + 1)

    # Valores de u(x,t)
    u = np.zeros(Nx + 1)  # u en j

    # Estructura de datos para el sistema lineal
    A = np.zeros((Nx - 1, Nx - 1))
    b = np.zeros(Nx - 1)
    for i in range(1, Nx - 2):
        A[i, i - 1] = -F
        A[i, i] = 1 + 2 * F
        A[i, i + 1] = -F
    A[0, 0] = A[Nx - 2, Nx - 2] = 1 + 2 * F
    A[0, 1] = A[Nx - 2, Nx - 3] = -F

    with graficar(x, t) as agregar_curva:
        # Condición inicial (y la dibujamos)
        up = I(x)
        agregar_curva(0, up)

        # Iteración en t (j)
        for j in range(1, Nt):
            # Calculamos b
            b = up[1:Nx]
            b[Nx - 2] += F * 2  # b[0] += F * 0 (condición de borde)

            # Resolvemos el sistema
            u[1:Nx] = linalg.solve(A, b)
            u[Nx] = 2

            # Trazamos una solución cada 10 pasos en j
            if not j % 10:
                agregar_curva(j * k, u)

            # Actualizamos los valores de up antes del próximo paso
            up = u


def resolver_ralas():
    """Método implícito utilizando matrices ralas."""
    # Puntos de resolución del problema
    Nx = 100  # Número de puntos de la malla en x
    Nt = 1000  # Número de puntos de la malla en t
    h = L / Nx  # Paso en x
    k = T / Nt  # Paso en t
    F = c * k / h ** 2  # Número de malla de Fourier
    print(f'{h=} | {k=} | {F=}')

    # Malla en x y t
    x = np.linspace(0, L, Nx + 1)
    t = np.linspace(0, T, Nt + 1)

    # Valores de u(x,t)
    u = np.zeros(Nx + 1)  # u en j

    # Calculamos la matriz rala
    diagonal = 1 + 2 * F
    superior = -F
    inferior = -F

    A = sparse.diags(
        diagonals=[diagonal, superior, inferior],
        offsets=[0, 1, -1],
        shape=(Nx - 1, Nx - 1),
        format='csr')
    print(A.todense())

    with graficar(x, t) as agregar_curva:
        # Condición inicial (y la dibujamos)
        up = I(x)
        agregar_curva(0, up)

        # Iteración en t (j)
        for j in range(1, Nt):
            # Calculamos b
            b = up[1:Nx]
            b[Nx - 2] += F * 2  # b[0] += F * 0 (condición de borde)

            # Resolvemos el sistema
            u[1:Nx] = sparse_linalg.spsolve(A, b)
            u[Nx] = 2

            # Trazamos una solución cada 10 pasos en j
            if not j % 10:
                agregar_curva(j * k, u)

            # Actualizamos los valores de up antes del próximo paso
            up = u


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    funcs = {
        'explicito': resolver_explicito,
        'implicito': resolver_implicito,
        'ralas': resolver_ralas,
    }
    parser.add_argument(
        'metodo', choices=funcs.keys(), help="El método para resolver las ecuaciones")
    args = parser.parse_args()
    func = funcs[args.metodo]
    func()

# Copyright 2020-2025 Facundo Batista y Manuel Carlevaro
# Licencia CC BY-NC-SA 4.0
# Para más info visitar https://github.com/facundobatista/libro-pyciencia/
