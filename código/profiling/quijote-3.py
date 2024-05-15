SIGNS = ["!", '"', "(", ")", ",", "-", ".", ":", ";", "?", "'", "[", "]", "¡", "«", "»", "¿"]


def _show_top10(count):
    print("Top 10:")
    for selection_round in range(1, 11):
        maxvalue = 0
        maxword = None
        for word, value in count.items():
            if value > maxvalue:
                maxvalue = value
                maxword = word

        print(f"{selection_round:2d}. {maxvalue:5d} {maxword}")
        del count[maxword]


def _count_words(all_lines):
    count = {}
    for line in all_lines:
        for word in line.split():
            try:
                value = count[word]
            except KeyError:
                value = 0
            count[word] = value + 1

    return count


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
    count = _count_words(all_lines)
    _show_top10(count)


word_count()

# Copyright 2020-2024 Facundo Batista y Manuel Carlevaro
# Licencia CC BY-NC-SA 4.0
# Para más info visitar https://github.com/facundobatista/libro-pyciencia/
