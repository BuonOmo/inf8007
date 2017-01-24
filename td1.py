import re
import sys

SYLL_CHAR = "a-zA-Zàéêèâôûù'"
WORD_CHAR = "a-zA-Zàéêèâôûù/"


class Text:
    def __init__(self, string, string_is_path=False):
        if string_is_path:
            try:
                self.text = open(string, "r", encoding="utf8").read()
            except FileNotFoundError as err:
                print('Wrong path', file=sys.stderr)
        else:
            self.text = string

    def count_words(self):
        return self.count_from_regex(r"[{}]+".format(WORD_CHAR))

    def count_sentences(self):
        return self.count_from_regex(r"\.(?:\.{2})?")

    def count_syllables(self):
        return self.count_from_regex(r"[{}]+".format(SYLL_CHAR))

    def count_from_regex(self, str_regex):
        return len(re.findall(str_regex, self.text))

    def process_lisibility(self):
        return 206.835 - 1.015 * (self.count_words() / self.count_sentences()) - 84.6 * (self.count_syllables() / self.count_words())


def main():
    text = Text("col-chabert.txt", string_is_path=True)
    syllable_count = text.count_syllables()
    word_count = text.count_words()
    sentence_count = text.count_sentences()

    print("""
    indice de lisibilité : {indice:.3f}
    nombre de syllabes   : {syllable_count}
    nombre de mots       : {word_count}
    nombre de phrases    : {sentence_count}
    """.format(
        indice=text.process_lisibility(),
        syllable_count=syllable_count,
        word_count=word_count,
        sentence_count=sentence_count
    ))


if __name__ == '__main__':
    main()
