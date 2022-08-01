import sys
from concurrent.futures import ProcessPoolExecutor

import scipy.io.wavfile as wavfile
from matplotlib import pyplot as plt, ticker
from scipy.fft import fft, fftfreq

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


def calculate_partial_fft(limits):
    lim_inf, lim_sup = limits
    partial_signal = signal[lim_inf:lim_sup]

    FFT = abs(fft(partial_signal))
    half_len = len(FFT) // 2
    FFT_side = FFT[1:half_len]  # positive-frequency terms, excluding zero
    return FFT_side


mid = len(signal) // 2
all_limits = [
    (0, mid),
    (mid, len(signal)),
]
with ProcessPoolExecutor() as executor:
    all_partial = executor.map(calculate_partial_fft, all_limits)

full_fft = sum(all_partial)
freqs = fftfreq(signal.size, Ts)[1: len(full_fft) + 1]
print("FFT terminado")

audible = (FREQ_MIN < freqs) & (freqs < FREQ_MAX)
FFT_side = full_fft[audible]
freqs = freqs[audible]
assert len(FFT_side) == len(freqs)
print("Audible seleccionado, cantidad de puntos:", len(FFT_side))

(fig,) = plt.plot(freqs[::100], FFT_side[::100], linewidth=0.3)
plt.xscale("log")
plt.xticks(TICKS)
plt.xlim([FREQ_MIN * 0.9, FREQ_MAX * 1.1])
plt.xlabel('Frecuencia (Hz)')
fig.axes.xaxis.set_major_formatter(ticker.ScalarFormatter())
plt.savefig("fft-mal.pdf")
print("Listo")

# Copyright 2020-2022 Facundo Batista y Manuel Carlevaro
# Licencia CC BY-NC-SA 4.0
# Para más info visitar https://github.com/facundobatista/libro-pyciencia/
