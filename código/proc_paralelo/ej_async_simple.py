import asyncio
import time


async def timings():
    print("A:", time.time())
    await asyncio.sleep(1)
    print("B:", time.time())

asyncio.run(timings())

# Copyright 2020-2024 Facundo Batista y Manuel Carlevaro
# Licencia CC BY-NC-SA 4.0
# Para más info visitar https://github.com/facundobatista/libro-pyciencia/
