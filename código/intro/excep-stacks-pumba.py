print("1. inicio")

def g():
    print("4a. antes en g")
    print("¿uno sobre cero?", 1 / 0)
    print("4b. después en g")

def f():
    print("3. antes en f")
    g()
    print("5. después en f")

print("2. antes en el módulo")
f()
print("6. después en el módulo")

print("7. fin")

# Copyright 2020-2021 Facundo Batista y Manuel Carlevaro
# Licencia CC BY-NC-SA 4.0
# Para más info visitar https://github.com/facundobatista/libro-pyciencia/
