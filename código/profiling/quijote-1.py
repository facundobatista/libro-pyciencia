SIGNS = ["!", '"', "(", ")", ",", "-", ".", ":", ";", "?", "'", "[", "]", "¡", "«", "»", "¿"]


def _show_top10(count_words, count_values):
    print("Top 10:")
    for selection_round in range(1, 11):
        maxvalue = 0
        maxpos = None
        for pos in range(len(count_values)):
            value = count_values[pos]
            if value > maxvalue:
                maxvalue = value
                maxpos = pos

        word = count_words[maxpos]
        print(f"{selection_round:2d}. {maxvalue:5d} {word}")
        del count_words[maxpos]
        del count_values[maxpos]


def _count_words(all_lines):
    count_words = []
    count_values = []
    for line in all_lines:
        for word in line.split():

            for sign in SIGNS:
                word = word.replace(sign, "")
            word = word.lower()

            try:
                word_position = count_words.index(word)
            except ValueError:
                count_words.append(word)
                count_values.append(1)
            else:
                old_value = count_values[word_position]
                count_values[word_position] = old_value + 1

    return count_words, count_values


def _filter_lines(text):
    all_lines = text.split("\n")
    start_pos = all_lines.index("El ingenioso hidalgo don Quijote de la Mancha")
    end_pos = all_lines.index("Fin")
    all_lines = all_lines[start_pos:end_pos + 1]
    return all_lines


def word_count():
    with open("quijote.txt", "rt", encoding="utf8") as fh:
        text = fh.read()
    all_lines = _filter_lines(text)
    count_words, count_values = _count_words(all_lines)
    _show_top10(count_words, count_values)


word_count()

# Copyright 2020-2025 Facundo Batista y Manuel Carlevaro
# Licencia CC BY-NC-SA 4.0
# Para más info visitar https://github.com/facundobatista/libro-pyciencia/
