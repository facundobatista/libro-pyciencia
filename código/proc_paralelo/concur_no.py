from urllib.request import urlopen

BASE = "https://raw.githubusercontent.com/facundobatista/libro-pyciencia/main/src/"
TEX_NAMES = ["integracion.tex", "intro.tex", "numpy.tex", "ordinarias.tex", "parciales.tex"]


class Adder:
    def __init__(self):
        self.total = 0

    def add(self, value):
        self.total += value


def downloader(tex_name, adder):
    url = BASE + tex_name
    u = urlopen(url)
    length = len(u.read())
    adder.add(length)


adder = Adder()
for tex_name in TEX_NAMES:
    downloader(tex_name, adder)
print("Done:", adder.total)

# Copyright 2020-2024 Facundo Batista y Manuel Carlevaro
# Licencia CC BY-NC-SA 4.0
# Para más info visitar https://github.com/facundobatista/libro-pyciencia/
