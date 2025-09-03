import time
from concurrent.futures import ProcessPoolExecutor
from itertools import chain


def factorizer(number):
    tini = time.time()
    orig_number = number
    results = []
    for factor in chain([2], range(3, number // 2 + 1, 2)):
        while number % factor == 0:
            results.append(factor)
            number = number // factor
        if factor > number:
            break
    tdelta = time.time() - tini
    print(f"{orig_number:16d}: {tdelta:7.2f}s")
    return results


inputs = [
    8919372543,
    2429192056233,
    23286190456122,
    51734095734,
    25301356,
    353061047130563,
    537334713453,
]
print("Ejecutando todo:")
tini = time.time()
with ProcessPoolExecutor(max_workers=4) as executor:
    all_results = executor.map(factorizer, inputs)
tdelta = time.time() - tini
print(f"Tiempo total: {tdelta:.2f}s")

print("Resultados:")
for number, result in zip(inputs, all_results):
    print(f"{number:16d}: {result}")

# Copyright 2020-2025 Facundo Batista y Manuel Carlevaro
# Licencia CC BY-NC-SA 4.0
# Para más info visitar https://github.com/facundobatista/libro-pyciencia/
