from collections import Counter

SIGNS = ["!", '"', "(", ")", ",", "-", ".", ":", ";", "?", "'", "[", "]", "¡", "«", "»", "¿"]


def _filter_lines(text):
    all_lines = text.split("\n")
    start_pos = all_lines.index("el ingenioso hidalgo don quijote de la mancha")
    end_pos = all_lines.index("fin")
    all_lines = all_lines[start_pos:end_pos + 1]
    return all_lines


def word_count():
    with open("quijote.txt", "rt", encoding="utf8") as fh:
        text = fh.read()

    for sign in SIGNS:
        text = text.replace(sign, "")
    text = text.lower()

    all_lines = _filter_lines(text)

    counter = Counter()
    for line in all_lines:
        counter.update(line.split())

    print("Top 10:")
    most_common = counter.most_common(10)
    for idx, (word, count) in enumerate(most_common, 1):
        print(f"{idx:2d}. {count:5d} {word}")


word_count()

# Copyright 2020-2024 Facundo Batista y Manuel Carlevaro
# Licencia CC BY-NC-SA 4.0
# Para más info visitar https://github.com/facundobatista/libro-pyciencia/
