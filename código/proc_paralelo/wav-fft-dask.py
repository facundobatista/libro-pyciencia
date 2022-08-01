import sys

import scipy.io.wavfile as wavfile
from dask.array import array
from dask.array.fft import fft
from matplotlib import pyplot as plt, ticker
from scipy.fft import fftfreq

FREQ_MIN, FREQ_MAX = 20, 20000
TICKS = [27.5, 55, 110, 220, 440, 880, 1760, 3520, 7040, 14080]

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

signal = array(signal).rechunk((1,))

FFT = abs(fft(signal))
half_len = len(FFT) // 2
FFT_side = FFT[1:half_len]  # positive-frequency terms, excluding zero
print("================ fft side", FFT_side[100:110])
freqs = fftfreq(signal.size, Ts)[1:half_len]
print("FFT terminado")

audible = (FREQ_MIN < freqs) & (freqs < FREQ_MAX)
FFT_side = FFT_side[audible]
freqs = freqs[audible]
assert len(FFT_side) == len(freqs)
print("Audible seleccionado, cantidad de puntos:", len(FFT_side))

(fig,) = plt.plot(freqs[::100], FFT_side[::100], linewidth=0.3)
plt.xscale("log")
plt.xticks(TICKS)
plt.xlabel('Frecuencia (Hz)')
fig.axes.xaxis.set_major_formatter(ticker.ScalarFormatter())
plt.savefig("fft4.pdf")
print("Listo")

# Copyright 2020-2022 Facundo Batista y Manuel Carlevaro
# Licencia CC BY-NC-SA 4.0
# Para más info visitar https://github.com/facundobatista/libro-pyciencia/
