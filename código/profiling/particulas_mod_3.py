import pandas as pd


def proc_file(filepath, center_x, center_y, radius):
    df = pd.read_csv(filepath, header=None, names=["x", "y", "radius"])
    df["included"] = (df.x - center_x) ** 2 + (df.y - center_y) ** 2 <= (df.radius + radius) ** 2
    return df["included"].value_counts()[True]

# Copyright 2020-2024 Facundo Batista y Manuel Carlevaro
# Licencia CC BY-NC-SA 4.0
# Para más info visitar https://github.com/facundobatista/libro-pyciencia/
