r"""

Greb is a command line tool to find meaning of words.

Usage: greb (<WORD> [-leyn] [-h | --help] | -d | -t | -w)

Options:
    -l --all        Lists everything
    -e --sen        Lists sentence
    -y --syn        Lists synonyms
    -n --ant        Lists antonyms
    -d --rdm        Displays a random from searched history
    -t --trn        Displays trending words from Merriam Webster
    -w --wrd        Displays the word of the day from Merriam Webster
    --version       Lists version
    -h --help       Lists help
"""
from __future__ import absolute_import
import json
import os
import requests
from bs4 import BeautifulSoup
from collections import OrderedDict
from colorama import Fore
from docopt import docopt
from os.path import expanduser
from random import SystemRandom

from . import opts

__version__ = '0.0.7'

HOME_PAGE_URL = 'http://www.merriam-webster.com'
BASE_URL = 'http://www.merriam-webster.com/dictionary/{word}'
HOME = expanduser('~')
MEANINGS_FILE_NAME = 'meanings.json'
FILE_PATH = os.path.join(HOME, MEANINGS_FILE_NAME)
SUGGESTION_CHECK_STRING = 'spelling suggestion below'

requests.packages.urllib3.disable_warnings()


def print_word(word):
    print('\n'+'#'*26)
    print('#{:^24}#'.format(word.upper()))
    print('#'*26)


def print_heading(heading, color=None):
    '''prints the heading for a section of output'''
    heading = heading.upper()
    color = color or eval(opts.COLOR.get(heading, 'Fore.WHITE'))
    print('')
    print(color + heading + Fore.RESET)
    print('')


def print_error_messages(msg):
    '''prints the error messgaes in red'''
    print(Fore.RED + msg + Fore.RESET)
    print('')


def print_result(result):
    for key, value in result.items():
        if value:
            if key in ('info_msg',):
                print(value)
            elif key not in ('word',):
                print_heading(key)
                for each in value:
                    print(each)
                print('')
            else:
                print_word(value)
        else:
            print_error_messages('Ohh! There are no {}s.'.format(key))


def write_meaning_to_file(meaning_as_json):
    '''saves the meaning json to the file `meanings.json` under home directory'''

    if not os.path.isfile(FILE_PATH):
        with open(FILE_PATH, 'w') as f:
            json.dump([], f)
    # first read the contents of file
    with open(FILE_PATH, 'r') as f:
        existing_meanings = json.load(f)

    # before appending check if the word exists or not
    existing_words = [each['word'] for each in existing_meanings]

    # append the current meaning only if it is not already there
    if meaning_as_json['word'] not in existing_words:
        existing_meanings.append(meaning_as_json)

        # write this to the same file
        with open(FILE_PATH, 'w') as f:
            json.dump(existing_meanings, f, indent=2)


def find_meaning_from_history():
    '''displays a random meaning from searched history.
       searched history is saved in a file `meanings.json` under home directory'''

    searched_meaning = OrderedDict()
    random_instance = SystemRandom()
    if os.path.isfile(FILE_PATH):
        with open(FILE_PATH, 'r') as f:
            all_meanings_searched = json.load(f)

        r_int = random_instance.randrange(len(all_meanings_searched))
        # to not break the existing meanings file, need to create a OrderedDict here
        # so that word comes before meaning key
        searched_meaning['word'] = all_meanings_searched[r_int]['word']
        searched_meaning['meaning'] = all_meanings_searched[r_int]['meaning']
    return searched_meaning


def find_sentences(tree, word):
    sentences = []
    try:
        sentence_html = tree.find('div', {'class': 'card-primary-content def-text'}).find_all('li')
    except (AttributeError, Exception) as e:  # noqa
        sentence_html = []
    if sentence_html:
        for i, each in enumerate(sentence_html, 1):
            each = (Fore.CYAN + str(i) + '. ' + Fore.RESET +
                    each.get_text().replace(word, Fore.CYAN + word + Fore.RESET))
            sentences.append(each)
    return sentences


def find_synonyms(tree):
    '''prints the synonyms for a given word'''
    synonyms = []
    synonyms_html = tree.find('div', {'class': 'card-box small-box related-box end'})
    if synonyms_html:
        synonyms_html = synonyms_html.find('div', {'class': 'definition-block'})
        synonyms_str = synonyms_html.get_text()
        synonyms_str = synonyms_str[synonyms_str.find('Synonyms') + len('Synonyms '): synonyms_str.find('Antonyms')]
        synonyms.append(synonyms_str)
    return synonyms


def find_antonyms(tree):
    '''prints the antonyms for a given word'''
    antonyms = []
    antonyms_html = tree.find('div', {'class': 'card-box small-box related-box end'})
    if antonyms_html:
        antonyms_html = antonyms_html.find('div', {'class': 'definition-block'})
        antonyms_str = antonyms_html.get_text()
        antonyms_str = antonyms_str[antonyms_str.find('Antonyms') + len('Antonyms '):
                                    antonyms_str.find('Related Words')]
        antonyms.append(antonyms_str)
    return antonyms


def find_trending_words(tree):
    '''prints the trending words on Merriam Webster'''
    trending_words = []
    try:
        trending_words_html = tree.find('div', {'class': 'wgt-wap-home-trending-items'}).find_all('li')
    except (AttributeError, Exception) as e:  # noqa
        trending_words_html = []

    if trending_words_html:
        for i, each in enumerate(trending_words_html, 1):
            word = each.find('p', {'class': 'title'}).get_text().strip()
            desc = each.find('p', {'class': 'blurb'}).get_text().strip()
            each = (Fore.RED + str(i) + ' ' + word + Fore.RESET +
                    ' --> ' + Fore.YELLOW + desc + Fore.RESET)
            trending_words.append(each)
    return trending_words


def find_word_of_the_day(tree):
    '''prints the word of the day from Merriam Webster'''
    word_of_day = []
    word_of_day_html = tree.find('div', {'class': 'wgt-wod-home'})
    if word_of_day_html:
        word = word_of_day_html.find('h4', {'class': 'wh-word'}).get_text().strip()
        meaning = word_of_day_html.find('p', {'class': 'wh-def-text'}).get_text().strip()
        word_of_day_str = (Fore.GREEN + word.upper() + Fore.RESET + ' : '
                           + Fore.YELLOW + meaning + Fore.RESET)
        word_of_day.append(word_of_day_str)
    return word_of_day


def find_suggestions(tree):
    '''lists the suggestions for a word in case of 404'''

    result = OrderedDict()
    if SUGGESTION_CHECK_STRING in tree.get_text():
        suggestion_html = tree.find_all('p', {'class': 'definition-inner-item with-sense'})
        if suggestion_html:
            info_msg = ('\n' + Fore.BLUE + 'It seems that you have not entered a valid word. '
                        'I know' + Fore.RESET + Fore.GREEN + ' To err is human.' +
                        Fore.RESET + Fore.BLUE + ' Hence the suggestions.' + Fore.RESET)
            result['info_msg'] = info_msg
            suggestion_str = ', '.join([each.get_text() for each in suggestion_html[0].find_all('a')])
            result['suggestion'] = [suggestion_str]
    else:
        result['info_msg'] = ("The word you've entered was not found. However I tried finding suggestions "
                              "thinking that you may have misspelled the word. But I failed miserably :(")
    return result


def read_page(url, timeout=5):
    try:
        response = requests.get(url, timeout=timeout, headers={'User-Agent':
                                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.7; rv:11.0) Gecko/20100101 Firefox/11.0'})
    except requests.exceptions.ConnectionError as e:  # noqa
        return(None, False)

    return(response, response.status_code)


def make_parse_tree(url):
    response, status_code = read_page(url)
    if status_code in [200, 404]:
        response = BeautifulSoup(response.text, 'html.parser')
    return (response, status_code)


def find_meaning(tree):

    meaning_div = (tree.select('ul > li > p.definition-inner-item')
                   or tree.select('div.card-primary-content')[0].find_all('p')
                   or tree.find_all('p', {'class': 'definition-inner-item with-sense'}))
    if meaning_div:
        meanings = []
        for each in meaning_div:
            each = each.get_text().strip().encode('ascii', 'ignore')
            meanings.append(each.decode('utf-8'))
    else:
        meanings = None

    return meanings


def greb(**kwargs):
    terminal_display = kwargs.get('display_terminal', False)
    if terminal_display:
        result = find_meaning_from_history()
        print_result(result)
    else:
        word = kwargs.get('word', None)
        if word:
            url = BASE_URL.format(word=word)
        else:
            url = HOME_PAGE_URL
        tree, status_code = make_parse_tree(url)
        result = OrderedDict()
        if status_code == requests.codes.ok:
            if kwargs.get('meaning', False):
                meanings = find_meaning(tree)
                result['word'] = word
                result['meaning'] = meanings
                if meanings:
                    write_meaning_to_file(result)
            if kwargs.get('sentence', False):
                sentences = find_sentences(tree, word)
                result['sentence'] = sentences
            if kwargs.get('synonym', False):
                synonyms = find_synonyms(tree)
                result['synonym'] = synonyms
            if kwargs.get('antonym', False):
                antonyms = find_antonyms(tree)
                result['antonym'] = antonyms
            if kwargs.get('trending_words', False):
                trending_words = find_trending_words(tree)
                result['trending words'] = trending_words
            if kwargs.get('word_of_day', False):
                word_of_day = find_word_of_the_day(tree)
                result['word of the day'] = word_of_day
        elif status_code == 404:
            result = find_suggestions(tree)
        else:
            result['info_msg'] = 'Can you please chech whether you Net Connection is working properly'
        print_result(result)


def main():
    '''greb is a command line tool to find meanings'''

    arguments = docopt(__doc__, version=__version__)
    options = {}
    if not arguments:
        print(__doc__)
    else:
        if arguments.get('-d') or arguments.get('--rdm'):
            options.update({
                'display_terminal': True
                })
        elif arguments.get('-t') or arguments.get('--trn'):
            options.update({
                'trending_words': True
                })
        elif arguments.get('-w') or arguments.get('--wrd'):
            options.update({
                'word_of_day': True
                })
        elif arguments['<WORD>']:
            options.update({
                'word': arguments['<WORD>'].lower().strip(),
                'meaning': True
                })
            if (arguments.get('-l') or arguments.get('--all')):
                flag_sentence, flag_synonym, flag_antonym = [True]*3
            else:
                flag_sentence = (arguments.get('-e') or arguments.get('--sen')) or False
                flag_synonym = (arguments.get('-y') or arguments.get('--syn')) or False
                flag_antonym = (arguments.get('-n') or arguments.get('--ant')) or False
            options.update({
                'sentence': flag_sentence,
                'synonym': flag_synonym,
                'antonym': flag_antonym,
                })
        greb(**options)


if __name__ == '__main__':
    main()
