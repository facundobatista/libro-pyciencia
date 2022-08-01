from concurrent.futures import ProcessPoolExecutor
from multiprocessing import RawArray

# dos secuencias de datos increiblemente grandes y complejas
input_a = RawArray('B', [1] * 12)
input_b = RawArray('B', [3] * 12)

# donde guardaremos los resultados
results = RawArray('B', [0] * 12)


def operator(limits):
    lim_inf, lim_sup = limits
    print(f"Operando entre {lim_inf} y {lim_sup}")
    for i in range(lim_inf, lim_sup):
        results[i] = input_a[i] + input_b[i]


all_limits = [
    (0, 4),
    (4, 8),
    (8, 12),
]
with ProcessPoolExecutor() as executor:
    list(executor.map(operator, all_limits))

print("Resultado final:", list(results))

# Copyright 2020-2022 Facundo Batista y Manuel Carlevaro
# Licencia CC BY-NC-SA 4.0
# Para más info visitar https://github.com/facundobatista/libro-pyciencia/
