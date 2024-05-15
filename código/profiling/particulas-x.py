import argparse
import importlib
import os


def main(basedir, outpath, center_x, center_y, radius, proc_file):
    outfh = open(outpath, "wt")
    for dirpath, dirnames, filenames in os.walk(basedir):
        for filename in filenames:
            count = proc_file(os.path.join(dirpath, filename), center_x, center_y, radius)
            outfh.write(f"{filename},{count}\n")
    outfh.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "modnum", type=int, help="el número de módulo a usar")
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

    mod = importlib.import_module(f"particulas_mod_{args.modnum}")

    main(args.dirpath, args.results_file, args.center_x, args.center_y, args.radius, mod.proc_file)

# Copyright 2020-2024 Facundo Batista y Manuel Carlevaro
# Licencia CC BY-NC-SA 4.0
# Para más info visitar https://github.com/facundobatista/libro-pyciencia/
