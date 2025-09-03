#!/usr/bin/env python3
"""
Solución de la ecuación de Poisson en 2D con condiciones de Dirichlet
para resolver un problema cuya solución es conocida.

    -∆(u) = f    en un cuadrado unitario
        0 = u_D  en la frontera

    u_D = 1 + x + 2 y^2
      f = -4
"""

import fenics as fe
import numpy as np

# Creamos la malla y definimos el espacio de funciones
mesh = fe.UnitSquareMesh(10, 10)
V = fe.FunctionSpace(mesh, 'P', 1)

# Definimos las condiciones de borde
u_D = fe.Expression("1 + x[0] + 2 * x[1]*x[1]", degree=2)


def boundary(x, on_boundary):
    return on_boundary


bc = fe.DirichletBC(V, u_D, boundary)

# Definimos el problema variacional
u = fe.TrialFunction(V)
v = fe.TestFunction(V)
f = fe.Constant(-4.0)
a = fe.dot(fe.grad(u), fe.grad(v)) * fe.dx
L = f * v * fe.dx

# Calculamos la solución
u = fe.Function(V)
fe.solve(a == L, u, bc)

# Guardamos la solución en un archivo con formato VTK
vtk_file = fe.File('poisson.pvd')
vtk_file << u

# Calculamos el error en la norma L2
error_L2 = fe.errornorm(u_D, u, 'L2')

# Calculamos los errores en los vértices
vertex_values_u_D = u_D.compute_vertex_values(mesh)
vertex_values_u = u.compute_vertex_values(mesh)
error_max = np.max(np.abs(vertex_values_u_D - vertex_values_u))

print(f'    Error L2 = {error_L2}')
print(f'Error máximo = {error_max}')

# Copyright 2020-2025 Facundo Batista y Manuel Carlevaro
# Licencia CC BY-NC-SA 4.0
# Para más info visitar https://github.com/facundobatista/libro-pyciencia/
