#!/usr/bin/env python3
"""Programa que integra el sistema masa-resorte-banda elástica."""

import argparse

import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import solve_ivp

# Parámetros del sistema
a, b = 17, 1  # Combinación de constantes elásticas
λ = 15.4  # Amplitud de la excitación periódica
μ = 0.75  # Frecuencia angular de la excitación periódica


def pos(x):
    """Devuelve x si x > 0, 0 en otro caso."""
    return max(x, 0)


def neg(x):
    """Devuelve -x si x < 0, 0 en otro caso."""
    return max(-x, 0)


def sistema(t, z):
    """Definición del sistema de ecuaciones diferenciales de primer orden.

    Argumentos:
        t: escalar que representa el tiempo
        z: lista con [y, dy/dt]

    Devuelve:
        [dy(t)/dt, d^2y(t)/dt^2]
    """
    y, yp = z  # yp = dy/dt
    return [yp, 10 + λ * np.sin(μ * t) - 0.01 * yp - a * pos(y) + b * neg(y)]


def main(archivo, usar_tex):
    """Punto de entrada principal."""
    print(f"Ejecutando con parámetros: {a=} {b=} {λ=} {µ=}")

    # Configure matplotlib
    matplotlib_config = {
        'font.size': 14,
        'axes.labelsize': 'large',
    }
    if usar_tex:
        # LaTeX Error: File `type1ec.sty' not found.
        matplotlib_config['text.usetex'] = True
    plt.rcParams.update(matplotlib_config)
    print(f"Config de matplotlib: {matplotlib_config}")

    # Array con la discretización del intervalo de tiempo en el que se calcula
    # la solución del sistema de EDOs
    t = np.linspace(0, 100, 10000)

    # Solución del sistema de EDOs
    sol = solve_ivp(sistema, [0, 100], [1, 0], t_eval=t)

    # Gráfico de la solución y del diagrama de fase
    fig, (ax0, ax1) = plt.subplots(1, 2)
    ax0.plot(sol.t, sol.y[0])
    ax0.set_ylim(8, -19)
    ax0.set_xlabel(r'$t$')
    ax0.set_ylabel(r'$y$')
    ax0.text(0.05, 0.9, 'a)', transform=ax0.transAxes, fontsize=18)
    ax1.plot(sol.y[0], sol.y[1])
    ax1.set_xlabel(r'$y$')
    ax1.set_ylabel(r"$dy/dt$")
    ax1.text(0.05, 0.9, 'b)', transform=ax1.transAxes, fontsize=18)

    if archivo is None:
        plt.show()
    else:
        plt.savefig(archivo)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--usar-tex", action="store_true", help="Usar TeX para los textos (default: False).")
    parser.add_argument(
        "--archivo",
        help="Graba la imagen al archivo indicado (default: abre una ventana para mostrarlo).")
    args = parser.parse_args()
    main(args.archivo, args.usar_tex)
