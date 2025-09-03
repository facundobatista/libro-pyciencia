import os

while True:
    try:
        text = input("\nOrden: ")
    except KeyboardInterrupt:
        print("\nSaliendo...")
        exit()
    words = text.strip().split()

    match words:

        case ["quit"]:
            print("Saliendo...")
            exit()

        case ["list"]:
            print("\n".join(os.listdir(".")))

        case ["stat", filename]:
            print(os.stat(filename))

        case ["rename", filename_from, filename_to]:
            os.rename(filename_from, filename_to)
            print("Done")

        case ["delete", filename_first, *filenames_rest]:
            for filename in [filename_first] + filenames_rest:
                os.unlink(filename)
            print("Done")

        case ["touch" | "create", filename]:
            open(filename, "wb").close()
            print("Done")

        case _:
            print("Error: orden incorrecta")

# Copyright 2020-2025 Facundo Batista y Manuel Carlevaro
# Licencia CC BY-NC-SA 4.0
# Para más info visitar https://github.com/facundobatista/libro-pyciencia/
