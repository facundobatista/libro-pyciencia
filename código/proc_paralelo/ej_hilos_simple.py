import random
import threading
import time

waits = []


def waiter():
    wait = random.randint(0, 100)
    time.sleep(wait / 100)
    waits.append(wait)


all_threads = []
for _ in range(5):
    th = threading.Thread(target=waiter)
    th.start()
    all_threads.append(th)

for th in all_threads:
    th.join()

print(waits)

# Copyright 2020-2024 Facundo Batista y Manuel Carlevaro
# Licencia CC BY-NC-SA 4.0
# Para más info visitar https://github.com/facundobatista/libro-pyciencia/
