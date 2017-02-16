#!/usr/bin/env python
# -*- coding: utf-8 -*-
from collections import defaultdict

from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer

from os import listdir
from os.path import isfile, join, basename
import re
import argparse

# --------------------------------------------------------------------------------- argument parsing
from numpy.dual import norm
from numpy.ma import dot


def parse_arguments():
    def acronym(v):
        try:
            return re.match("^[A-Z]{3}\d{4}\w?$", v).group(0)
        except:
            raise argparse.ArgumentTypeError('"{}" n’est pas un sigle de cours correct'.format(v))

    parser = argparse.ArgumentParser(description='Script du TD2, similarité de textes')
    parser.add_argument('acronym', metavar='SIGLE', type=acronym, default='INF8007', nargs='?',
                        help='Nom du cours à verifier')
    parser.add_argument('-d', type=str, dest='path', default='02/PolyHEC',
                        help='Chemin vers la liste de fichiers')

    return parser.parse_args()


# -------------------------------------------------------------------------------------------- utils
def parse_course(path, do_raise=False):
    """ Parse a course file to retrieve it’s title and description, may raise error if file is
        corrupted or not found """
    with open(path) as stream:
        title = stream.readline()[12:].strip()
        description = stream.readline()[18:].strip()
        leftover = stream.read()
        if leftover:
            if do_raise:
                raise Exception('File not totally parsed', path, leftover)
            description += leftover.strip()
    return title, description


# -------------------------------------------------------------------------------------- text parser
class Parser:
    WORD_SEPARATOR = r'(?:(?:&nbsp)?[\s.,:;?!()\\/\'\"])+'

    def __init__(self, language='french'):
        self.stopwords = set(stopwords.words(language))
        self.stemmer = SnowballStemmer(language=language)

    def tokenise(self, string, remove_stop_words=False, stem=False):
        """ break string up into tokens """
        words = re.split(self.WORD_SEPARATOR, string.strip().lower())
        if remove_stop_words:
            words = filter(lambda w: w not in self.stopwords, words)
        if stem:
            words = map(self.stemmer.stem, words)
        # usage of map  and filter instead of array comprehension allows to iterate only once through
        # the list
        return list(words)

    def count_terms(self, list_):
        rv = defaultdict(lambda: 0)
        for word in list_:
            rv[word] += 1
        return dict(rv)


# ------------------------------------------------------------------------------------ search engine
class SearchEngine:
    def __init__(self, files, language='french'):
        self.files = files
        self.parser = Parser(language=language)
        # list of all uniq words, eventually optimised with stemming and stopwords sorting.
        all_words_string = ' '.join(parse_course(file)[1] for file in files)
        word_list = set(self.parser.tokenise(all_words_string))
        self.words_index = {word: index for (index, word) in enumerate(word_list)}
        self.vectors = {}
        for file in files:
            vector = [0] * len(self.words_index)
            for word in self.parser.tokenise(parse_course(file)[1]):
                vector[self.words_index[word]] += 1
            self.vectors[basename(file)[:-4]] = vector

    def _cosine(self, a, b):
        return float(dot(a, b) / (norm(a) * norm(b)))

    def search(self, acronym):
        search_vec = self.vectors[acronym]
        return {acr: self._cosine(search_vec, other_vec) for (acr, other_vec) in
                self.vectors.items() if acronym != acr}


# --------------------------------------------------------------------------------- main application
def main(path):
    files = [join(path, f) for f in listdir(path) if isfile(join(path, f))]


if __name__ == '__main__':
    args = parse_arguments()
    main(path=args.path)
