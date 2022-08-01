import asyncio
import random
from datetime import datetime


async def sleeper(sleeper_id):
    delay = random.random() * 5  # random float between 0 and 5
    print(f"Arranca {sleeper_id} a las {datetime.now():%X.%f}")
    await asyncio.sleep(delay)
    print(f"Termina {sleeper_id} a las {datetime.now():%X.%f}")
    return delay


async def main():
    slept = await sleeper(1)
    print(f"Durmió: {slept:.3f}s")

asyncio.run(main())

# Copyright 2020-2022 Facundo Batista y Manuel Carlevaro
# Licencia CC BY-NC-SA 4.0
# Para más info visitar https://github.com/facundobatista/libro-pyciencia/
