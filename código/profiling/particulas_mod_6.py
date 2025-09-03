from numba import njit
from numba.typed import List


@njit
def _proc(data, center_x, center_y, radius):
    count = 0
    for particle_x, particle_y, particle_radius in data:
        dist_centers = (particle_x - center_x) ** 2 + (particle_y - center_y) ** 2
        if dist_centers <= (radius + particle_radius) ** 2:
            count += 1
    return count


def proc_file(filepath, center_x, center_y, radius):
    with open(filepath, "rb") as fh:
        data = List()
        for line in fh:
            particle_x, particle_y, particle_radius = map(float, line.split(b","))
            data.append((particle_x, particle_y, particle_radius))
        return _proc(data, center_x, center_y, radius)

# Copyright 2020-2025 Facundo Batista y Manuel Carlevaro
# Licencia CC BY-NC-SA 4.0
# Para más info visitar https://github.com/facundobatista/libro-pyciencia/
