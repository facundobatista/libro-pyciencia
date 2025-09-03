import pytest

from mod import adder


@pytest.mark.parametrize("a, b, c", [
    (3, 5, 8),
    (5, 3, 8),
    (0, 1000, 1000),
    (-23, 0, -23),
    (87, -87, 0),
    (-15, -15, -30),
])
def test_numbers(a, b, c):
    result = adder(a, b)
    assert result == c

# Copyright 2020-2025 Facundo Batista y Manuel Carlevaro
# Licencia CC BY-NC-SA 4.0
# Para más info visitar https://github.com/facundobatista/libro-pyciencia/
