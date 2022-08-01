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
    tasks = [asyncio.create_task(sleeper(n)) for n in range(3)]
    print("Corrutinas creadas")
    results = await asyncio.gather(*tasks)
    print("Durmieron:")
    for idx, slept in enumerate(results):
        print(f"{idx:4d}: {slept:.3f}s")

asyncio.run(main())

# Copyright 2020-2022 Facundo Batista y Manuel Carlevaro
# Licencia CC BY-NC-SA 4.0
# Para más info visitar https://github.com/facundobatista/libro-pyciencia/
