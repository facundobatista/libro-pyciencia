import argparse
import os


def proc_file(filepath, center_x, center_y, radius):
    count = 0
    with open(filepath, "rt") as fh:
        for line in fh:
            particle_x, particle_y, particle_radius = map(float, line.strip().split(","))
            dist_centers = (particle_x - center_x) ** 2 + (particle_y - center_y) ** 2
            if dist_centers <= (radius + particle_radius) ** 2:
                count += 1
    return count


def main(basedir, outpath, center_x, center_y, radius):
    outfh = open(outpath, "wt")
    for dirpath, dirnames, filenames in os.walk(basedir):
        for filename in filenames:
            count = proc_file(os.path.join(dirpath, filename), center_x, center_y, radius)
            outfh.write(f"{filename},{count}\n")
    outfh.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "dirpath", help="directorio base a procesar")
    parser.add_argument(
        "results_file", help="nombre del archivo donde guardar los resultados")
    parser.add_argument(
        "center_x", type=float, help="coordenada X del centro del circulo a filtrar")
    parser.add_argument(
        "center_y", type=float, help="coordenada Y del centro del circulo a filtrar")
    parser.add_argument(
        "radius", type=float, help="radio del circulo a filtrar")
    args = parser.parse_args()

    main(args.dirpath, args.results_file, args.center_x, args.center_y, args.radius)

# Copyright 2020-2025 Facundo Batista y Manuel Carlevaro
# Licencia CC BY-NC-SA 4.0
# Para más info visitar https://github.com/facundobatista/libro-pyciencia/
