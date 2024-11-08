#!/usr/bin/env python3

from math import cos, log, pi

import numpy as np
import matplotlib.pyplot as plt
from scipy import optimize

n_puntos = 300
xs = np.linspace(-3, 3, n_puntos)
ys = np.linspace(-5, 15, n_puntos)
X, Y = np.meshgrid(xs, ys)
Z1 = Y - X**2 + X * np.cos(pi * X)
Z2 = Y - (X - 2) * (X + 2) * X - np.log((Y + 1)**4)
fig, ax = plt.subplots()
CS1 = ax.contour(X, Y, Z1, levels=[0], colors=['royalblue'])
ax.clabel(CS1, levels=[0], fmt={0: r'$f_1$'}, fontsize=12)
CS2 = ax.contour(X, Y, Z2, levels=[0], colors=['maroon'])
ax.clabel(CS2, levels=[0], fmt={0: r'$f_2$'})


def f(x):
    return [
        x[1] - x[0]**2 + x[0] * cos(pi * x[0]),
        x[1] - x[0]**3 + 4 * x[0] - log((x[1] + 1)**4)
    ]


x_guess = [[-2.0, 5.0], [0, 0], [1.5, 2.0]]
sols = []
for x_g in x_guess:
    sol = optimize.root(f, x_g, method='hybr')
    print(sol.message)
    print(f'x: [{sol.x[0]:.3f}, {sol.x[1]:.3f}] -- root: {f(sol.x)}')
    sols.append(sol.x)

colors = ['r', 'b', 'g']
for i, s in enumerate(sols):
    ax.plot(s[0], s[1], colors[i] + '*', markersize=15)

n_trial = 100
xs = np.linspace(-3, 3, n_trial)
ys = np.linspace(-5, 15, n_trial)
n_div = 0
for xc in xs:
    for yc in ys:
        ss = optimize.root(f, [xc, yc], method='hybr')
        if ss.success:
            idx = (abs(sols - ss.x)**2).sum(axis=1).argmin()
            ax.plot(xc, yc, marker='.', color=colors[idx], alpha=0.15)
        else:
            n_div += 1
print(f'Proporción de no convergencia: {n_div / n_trial**2:.4f}')
plt.ylim([-5, 15])
plt.savefig('sol_hybr.pdf')

# Copyright 2020-2024 Facundo Batista y Manuel Carlevaro
# Licencia CC BY-NC-SA 4.0
# Para más info visitar https://github.com/facundobatista/libro-pyciencia/
