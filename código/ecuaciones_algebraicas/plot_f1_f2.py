#!/usr/bin/env python3

from math import pi

import numpy as np
import matplotlib.pyplot as plt

n_puntos = 300
xs = np.linspace(-3, 3, n_puntos)
ys = np.linspace(-5, 15, n_puntos)
X, Y = np.meshgrid(xs, ys)
Z1 = Y - X**2 + X * np.cos(pi * X)
Z2 = Y - (X - 2) * (X + 2) * X - np.log((Y + 1) ** 4)
fig, ax = plt.subplots()
CS1 = ax.contour(X, Y, Z1, levels=[0], colors=['royalblue'])
ax.clabel(CS1, levels=[0], fmt={0: r'$f_1$'}, fontsize=12)
CS2 = ax.contour(X, Y, Z2, levels=[0], colors=['maroon'])
ax.clabel(CS2, levels=[0], fmt={0: r'$f_2$'})
plt.savefig('f1_f2_ceros.pdf')

# Copyright 2020-2024 Facundo Batista y Manuel Carlevaro
# Licencia CC BY-NC-SA 4.0
# Para más info visitar https://github.com/facundobatista/libro-pyciencia/
