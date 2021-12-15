#!/usr/bin/env python3

import matplotlib.pyplot as plt
import numpy as np
import sympy as sym
plt.rcParams.update({
    "text.usetex": True,
    "axes.labelsize": 18,
    "xtick.labelsize": 14,
    "ytick.labelsize":14})

def f(x):
    return 400 * x**5 - 900 * x**4 + 675 * x**3 - 200 * x**2 + 25 * x + 0.2

a, b, c = 0, 0.8, 4 # Límites de integración y escala vertical
xs = sym.Symbol('x')
fs = f(xs)
int_sym = sym.integrate(fs, (xs, a, b))
print(f'Integral sympy = {int_sym}')

n_mc = 100 # Puntos de Monte Carlo
rng = np.random.default_rng(seed=13)
x = rng.uniform(a, b, n_mc)
y = rng.uniform(a, c, n_mc)

mask = y < f(x) # Selección de puntos de MC debajo de la curva
no_mask = ~mask   # Selección de puntos de MC arriba de la curva
int_MC = y[mask].size / n_mc * (b - a) * c
print(fr'   Integral MC = {int_MC}')
print(f'Diferencia porcentual = {(int_MC - int_sym)/int_sym * 100:.3f} %')

x_plot = np.linspace(a, b, 200) # Coordenadas para graficar f(x)
plt.plot(x_plot, f(x_plot), c='tab:blue', lw=3)
plt.scatter(x[mask], y[mask], c='tab:blue')
plt.scatter(x[no_mask], y[no_mask], c='tab:red')

plt.xlabel(r'$x$')
plt.ylabel(r'$f(x)$')
plt.xlim([a, b])
plt.ylim([a, c])
plt.savefig('mc-1d.pdf', bbox_inches='tight')

# Copyright 2020-2021 Facundo Batista y Manuel Carlevaro
# Licencia CC BY-NC-SA 4.0
# Para más info visitar https://github.com/facundobatista/libro-pyciencia/
