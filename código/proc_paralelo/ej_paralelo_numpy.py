import numpy as np
from concurrent.futures import ProcessPoolExecutor
from multiprocessing import shared_memory

# el tamaño de nuestras secuencias de datos increiblemente grandes y complejas
size = 12

# creamos toda la memoria compartida que vamos a usar (para los tres arreglos)
array_size = np.int8().size * size
shared_memory = shared_memory.SharedMemory(create=True, size=array_size * 3)

# los dos arreglos de entrada (con sus valores), y el de los resultados
input_a = np.ndarray((size,), dtype=np.int8, buffer=shared_memory.buf)
input_a.fill(1)
input_b = np.ndarray((size,), dtype=np.int8, buffer=shared_memory.buf, offset=array_size)
input_b.fill(3)
results = np.ndarray((size,), dtype=np.int8, buffer=shared_memory.buf, offset=array_size * 2)


def operator(limits):
    l_inf, l_sup = limits
    print(f"Operando entre {l_inf} y {l_sup}")
    results[l_inf:l_sup] = input_a[l_inf:l_sup] + input_b[l_inf:l_sup]


all_limits = [
    (0, 4),
    (4, 8),
    (8, 12),
]
with ProcessPoolExecutor() as executor:
    list(executor.map(operator, all_limits))

print("Resultado final:", results)

# cerramos y liberamos los recursos de memoria compartida
shared_memory.close()
shared_memory.unlink()

# Copyright 2020-2022 Facundo Batista y Manuel Carlevaro
# Licencia CC BY-NC-SA 4.0
# Para más info visitar https://github.com/facundobatista/libro-pyciencia/
