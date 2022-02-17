#!/usr/bin/env fades

import sys

import tinytag  # fades

tag = tinytag.TinyTag.get(sys.argv[1])
print("{!r} por {}".format(tag.title, tag.artist))

# Copyright 2020-2022 Facundo Batista y Manuel Carlevaro
# Licencia CC BY-NC-SA 4.0
# Para más info visitar https://github.com/facundobatista/libro-pyciencia/
