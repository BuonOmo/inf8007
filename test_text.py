from unittest import TestCase, main
from td1 import Text


class TestText(TestCase):
    def test_count_words(self):
        t = lambda to_test: Text(to_test).count_words()
        self.assertEqual(t('Bon/jour, mon/de!'), 2, "Simple case")
        self.assertEqual(t('sau/te-mou/ton'), 2, "Composed word")
        self.assertEqual(t(u"l'arbre"), 2, "Apostrophe separated words")
        self.assertEqual(t(u"àéèâôûùê"), 1, "French stuff")

    def test_count_sentences(self):
        t = lambda to_test: Text(to_test).count_sentences()
        self.assertEqual(t('Non.'), 1, "Simple case")
        self.assertEqual(t('Non... Mais en fait si.'), 2, "...")

    def test_count_syllables(self):
        t = lambda to_test: Text(to_test).count_syllables()

    def test_count_from_regex(self):
        self.assertEqual(Text('abcde').count_from_regex(r'.'), 5, "Simple case is enough")

    def test_process_lisibility(self):
        t = lambda to_test: Text(to_test).process_lisibility()
        self.assertAlmostEqual(t('Tout est dit.'), 119.19, msg="Simple case is enought")

if __name__ == '__main__':
    main()

