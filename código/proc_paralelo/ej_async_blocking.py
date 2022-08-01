import asyncio
import itertools
import sys
import time


async def spinner():
    ticks = itertools.cycle("|/-\\")
    while True:
        print(f"{next(ticks)}\r", end="", flush=True)
        await asyncio.sleep(.2)


async def generic_work_async():
    await asyncio.sleep(3)
    return 5


def generic_work_blocking():
    time.sleep(3)
    return 7


async def main(option):
    print("Comienzo")
    spinner_task = asyncio.create_task(spinner())

    if option == "1":
        print("Durmiendo modo async, ¡perfecto!")
        result = await generic_work_async()
    elif option == "2":
        print("Bloqueando todo, está mal :(")
        result = generic_work_blocking()
    else:
        print("Bloqueando, pero en un hilo (no traba todo)")
        result = await asyncio.to_thread(generic_work_blocking)

    spinner_task.cancel()
    print(f"Final; {result=}")

if len(sys.argv) != 2 or sys.argv[1] not in ["1", "2", "3"]:
    print("Usar: python3 ej_async_blocking.py {1|2|3}")
    sys.exit()

asyncio.run(main(sys.argv[1]))

# Copyright 2020-2022 Facundo Batista y Manuel Carlevaro
# Licencia CC BY-NC-SA 4.0
# Para más info visitar https://github.com/facundobatista/libro-pyciencia/
