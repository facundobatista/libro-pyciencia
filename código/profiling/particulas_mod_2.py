def proc_file(filepath, center_x, center_y, radius):
    count = 0
    with open(filepath, "rb") as fh:
        for line in fh:
            particle_x, particle_y, particle_radius = map(float, line.split(b","))
            dist_centers = (particle_x - center_x) ** 2 + (particle_y - center_y) ** 2
            if dist_centers <= (radius + particle_radius) ** 2:
                count += 1
    return count

# Copyright 2020-2025 Facundo Batista y Manuel Carlevaro
# Licencia CC BY-NC-SA 4.0
# Para más info visitar https://github.com/facundobatista/libro-pyciencia/
