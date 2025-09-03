import asyncio

import aiohttp

BASE = "https://raw.githubusercontent.com/facundobatista/libro-pyciencia/main/src/"
TEX_NAMES = ["integracion.tex", "intro.tex", "numpy.tex", "ordinarias.tex", "parciales.tex"]


class Adder:
    def __init__(self):
        self.total = 0

    def add(self, value):
        self.total += value


async def downloader(tex_name, adder):
    url = BASE + tex_name
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            content = await resp.read()
    adder.add(len(content))


async def main():
    adder = Adder()
    all_coroutines = []
    for tex_name in TEX_NAMES:
        coroutine = downloader(tex_name, adder)
        all_coroutines.append(coroutine)
    await asyncio.gather(*all_coroutines)
    print("Done:", adder.total)


asyncio.run(main())

# Copyright 2020-2025 Facundo Batista y Manuel Carlevaro
# Licencia CC BY-NC-SA 4.0
# Para más info visitar https://github.com/facundobatista/libro-pyciencia/
