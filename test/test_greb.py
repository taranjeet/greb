from __future__ import unicode_literals, absolute_import
import StringIO
import sys
import unittest

from greb import meaning as greb

from . import data


class TestGreb(unittest.TestCase):

    def test_read_page(self):
        for each in data.READ_PAGE_DATA:
            url = each.get('url')
            expected_status_code = each.get('status_code')
            response, status_code = greb.read_page(url)
            self.assertEqual(status_code, expected_status_code)

    def test_find_meaning(self):
        for each_word, each_word_meaning in data.INPUT_WORDS['MEANING'].items():
            tree, status_code = greb.make_parse_tree(data.COMMON['URLS']['base'].format(word=each_word))
            self.assertEqual(status_code, data.COMMON['STATUS_CODE']['ok'])

            meaning = greb.find_meaning(tree)
            self.assertEqual(meaning, each_word_meaning)

    def test_find_sentences(self):
        for each_word, each_word_sentence in data.INPUT_WORDS['SENTENCE'].items():
            tree, status_code = greb.make_parse_tree(data.COMMON['URLS']['base'].format(word=each_word))
            self.assertEqual(status_code, data.COMMON['STATUS_CODE']['ok'])

            sentence = greb.find_sentences(tree, each_word)
            self.assertEqual(sentence, each_word_sentence)

    def test_find_synonyms(self):
        for each_word, each_word_synonym in data.INPUT_WORDS['SYNONYM'].items():
            tree, status_code = greb.make_parse_tree(data.COMMON['URLS']['base'].format(word=each_word))
            self.assertEqual(status_code, data.COMMON['STATUS_CODE']['ok'])

            synonym = greb.find_synonyms(tree)
            self.assertEqual(synonym, each_word_synonym)

    def test_find_antonyms(self):
        for each_word, each_word_antonym in data.INPUT_WORDS['ANTONYM'].items():
            tree, status_code = greb.make_parse_tree(data.COMMON['URLS']['base'].format(word=each_word))
            self.assertEqual(status_code, data.COMMON['STATUS_CODE']['ok'])

            antonym = greb.find_antonyms(tree)
            self.assertEqual(antonym, each_word_antonym)

    def test_find_trending_words(self):
        tree, status_code = greb.make_parse_tree(data.COMMON['URLS']['home'])
        self.assertEqual(status_code, data.COMMON['STATUS_CODE']['ok'])

        trending_words = greb.find_trending_words(tree)
        self.assertEqual(len(trending_words), 5)

    def test_find_word_of_the_day(self):
        tree, status_code = greb.make_parse_tree(data.COMMON['URLS']['home'])
        self.assertEqual(status_code, data.COMMON['STATUS_CODE']['ok'])

        word_of_day = greb.find_word_of_the_day(tree)
        self.assertEqual(len(word_of_day), 1)

    def test_find_suggestions(self):
        for each_word, each_word_dict in data.MISSPELLED_WORDS.items():
            expected_status_code = each_word_dict.get('status_code')
            suggestion_string = each_word_dict.get('suggestion_string')
            suggestion_key = each_word_dict.get('suggestion_key')
            # expected_suggestions = each_word_dict.get('suggestions')

            tree, status_code = greb.make_parse_tree(data.COMMON['URLS']['base'].format(word=each_word))
            self.assertEqual(status_code, expected_status_code)

            self.assertIn(suggestion_string, tree.get_text())

            result = greb.find_suggestions(tree)
            self.assertIn(suggestion_key, result)
            # suggestions = result.get('suggestion')
            # self.assertEqual(suggestions, expected_suggestions)

    def test_print_heading(self):
        captured_output = StringIO.StringIO()
        sys.stdout = captured_output
        greb.print_heading(data.PRINT_FUNCTION['print_heading']['input'])
        sys.stdout = sys.__stdout__
        self.assertEqual(captured_output.getvalue(), data.PRINT_FUNCTION['print_heading']['output'])


if __name__ == '__main__':
    unittest.main()
