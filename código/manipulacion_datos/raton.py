import struct

with open("/dev/input/mice", "rb") as fh:  # needs root permissions
    while True:
        try:
            data = fh.read(3)
            button, x, y = struct.unpack(">bbb", data)

            left = button & 0x1
            right = button & 0x2
            middle = button & 0x4

            print(f"{x=}, {y=}, {left=}, {middle=}, {right=}")
        except KeyboardInterrupt:
            break

# Copyright 2020-2023 Facundo Batista y Manuel Carlevaro
# Licencia CC BY-NC-SA 4.0
# Para más info visitar https://github.com/facundobatista/libro-pyciencia/
