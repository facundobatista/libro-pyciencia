import numpy as np
import sys
from concurrent.futures import ProcessPoolExecutor
from multiprocessing import shared_memory, Lock

import scipy.io.wavfile as wavfile
from matplotlib import pyplot as plt, ticker
from scipy.fft import fft, fftfreq

FREQ_MIN, FREQ_MAX = 20, 20000
TICKS = [27.5, 55, 110, 220, 440, 880, 1760, 3520, 7040, 14080]
MULTPARTS = 8

src = sys.argv[1]
print("Cargando", src)
fs_rate, signal = wavfile.read(src)
print("Frecuencia de muestreo:", fs_rate)

q_channels = len(signal.shape)
print("Canales:", q_channels)

if q_channels == 2:
    signal = signal.sum(axis=1) / 2
assert signal.ndim == 1
Ts = 1.0 / fs_rate
print("Duración [s]:", len(signal) * Ts)

signal_bytes_length = signal.itemsize * signal.size
signal_mem = shared_memory.SharedMemory(create=True, size=signal_bytes_length)
shared_signal = np.ndarray(signal.shape, dtype=signal.dtype, buffer=signal_mem.buf)
shared_signal[:] = signal
del signal

result_size = shared_signal.size // MULTPARTS // 2 - 1
result_bytes_length = shared_signal.itemsize * result_size
result_mem = shared_memory.SharedMemory(create=True, size=result_bytes_length)
shared_result = np.ndarray((result_size,), dtype=shared_signal.dtype, buffer=result_mem.buf)


def calculate_partial_fft(offset):
    global shared_result

    FFT = abs(fft(shared_signal[offset::MULTPARTS]))
    half_len = len(FFT) // 2
    useful = FFT[1:half_len]  # positive-frequency terms, excluding zero
    with result_lock:
        shared_result += useful


result_lock = Lock()
with ProcessPoolExecutor() as executor:
    executor.map(calculate_partial_fft, list(range(MULTPARTS)))

freqs = fftfreq(shared_signal.size, Ts)[1: len(shared_result) + 1]
print("FFT terminado")

audible = (FREQ_MIN < freqs) & (freqs < FREQ_MAX)
FFT_side = shared_result[audible]
freqs = freqs[audible]
assert len(FFT_side) == len(freqs)
print("Audible seleccionado, cantidad de puntos:", len(FFT_side))

(fig,) = plt.plot(freqs[::100], FFT_side[::100], linewidth=0.3)
plt.xscale("log")
plt.xticks(TICKS)
plt.xlim([FREQ_MIN * 0.9, FREQ_MAX * 1.1])
plt.xlabel('Frecuencia (Hz)')
fig.axes.xaxis.set_major_formatter(ticker.ScalarFormatter())
plt.savefig("fft-paralelo-ok.pdf")

for mem in (signal_mem, result_mem):
    mem.close()
    mem.unlink()
print("Listo")

# Copyright 2020-2025 Facundo Batista y Manuel Carlevaro
# Licencia CC BY-NC-SA 4.0
# Para más info visitar https://github.com/facundobatista/libro-pyciencia/
