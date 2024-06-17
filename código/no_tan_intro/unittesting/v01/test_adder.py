from mod import adder  # importamos la función a testear


def test_simple():
    result = adder(3, 5)
    assert result == 8


def test_reverse():
    result = adder(5, 3)
    assert result == 8

# Copyright 2020-2024 Facundo Batista y Manuel Carlevaro
# Licencia CC BY-NC-SA 4.0
# Para más info visitar https://github.com/facundobatista/libro-pyciencia/
