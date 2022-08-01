import random
import threading
import time


class Waiter(threading.Thread):

    waits = []

    def run(self):
        wait = random.randint(0, 100)
        time.sleep(wait / 100)
        self.waits.append(wait)


all_threads = []
for _ in range(5):
    th = Waiter()
    th.start()
    all_threads.append(th)

for th in all_threads:
    th.join()

print(Waiter.waits)

# Copyright 2020-2022 Facundo Batista y Manuel Carlevaro
# Licencia CC BY-NC-SA 4.0
# Para más info visitar https://github.com/facundobatista/libro-pyciencia/
