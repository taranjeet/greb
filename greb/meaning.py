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

import json
import os
import requests
import sys
from bs4 import BeautifulSoup
from colorama import Fore
from docopt import docopt
from os.path import expanduser
from random import SystemRandom

__version__ = '0.0.6'

HOME_PAGE_URL = 'http://www.merriam-webster.com'
BASE_URL = 'http://www.merriam-webster.com/dictionary/{word}'
HOME = expanduser('~')
MEANINGS_FILE_NAME = 'meanings.json'
FILE_PATH = os.path.join(HOME, MEANINGS_FILE_NAME)

requests.packages.urllib3.disable_warnings()


def print_heading(heading, color):
    '''prints the heading for a section of output'''

    print("")
    print(color + heading + Fore.RESET)
    print("")


def print_error_messages(msg):
    '''prints the error messgaes in red'''

    print(Fore.RED + msg + Fore.RESET)


def find_meaning(tree, word):
    '''prints the meaning corresponding to a word'''

    meanings = tree.find("div", {"class": "definition-block def-text"})
    temp_json = {
        "word": word,
        "meaning": [],
    }
    temp_meaning_list = []
    found_meaning = False
    if meanings:
        found_meaning = True
        for each in meanings.find_all("p"):
            temp_meaning_list.append(each.get_text().strip())
    else:
        meanings = tree.find_all("p", {"class": "definition-inner-item with-sense"})
        if meanings:
            found_meaning = True
            for each in meanings:
                if ':' in each.get_text():
                    each = each.get_text().split(':')[1].replace(u'\xc2', ' ').replace(u'\xa0', ' ')
                    if len(each.strip()) > 0:
                        temp_meaning_list.append(': ' + each.strip().encode('utf8'))
                else:
                    temp_meaning_list.append(each.get_text().encode('utf8').strip())
    if not found_meaning:
        print_error_messages("Unable to find meaning for this word. Are you sure its spelled right?")
    else:
        temp_json['meaning'] = temp_meaning_list
        print_meaning_to_console(temp_json)
        write_meaning_to_file(temp_json)
    return found_meaning


def print_meaning_to_console(meaning_as_json):
    '''outputs the meaning json to the console'''

    print_heading(meaning_as_json['word'].upper(), Fore.YELLOW)
    for each_meaning in meaning_as_json.get('meaning'):
        print(each_meaning)


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


def get_meaning_for_terminal():
    '''displays a random meaning from searched history.
       searched history is saved in a file `meanings.json` under home directory'''

    random_instance = SystemRandom()
    if os.path.isfile(FILE_PATH):
        with open(FILE_PATH, 'r') as f:
            all_meanings = json.load(f)

        r_int = random_instance.randrange(len(all_meanings))
        print_meaning_to_console(all_meanings[r_int])


def display_sentences(tree, word):
    '''prints the sentences showing the use of a word'''

    sentences = tree.find("div", {"class": "card-primary-content def-text"})
    if sentences:
        print_heading('SENTENCE', Fore.GREEN)
        for each in sentences.find_all("li"):
            print(each.get_text().replace(word, Fore.CYAN + word + Fore.RESET))
    else:
        print_error_messages("Oops! There are no sentences to display. Why not frame your own?")


def display_synonyms(tree):
    '''prints the synonyms for a given word'''

    syn_outer_div = tree.find("div", {"class": "card-box small-box related-box end"})
    if syn_outer_div:
        syn_inner_div = syn_outer_div.find("div", {"class": "definition-block"})
        synonyms = syn_inner_div.get_text()
        print_heading('SYNONYM', Fore.BLUE)
        print(synonyms[synonyms.find("Synonyms") + len("Synonyms "): synonyms.find("Antonyms")])
    else:
        print_error_messages("Ohh! There are no synonyms.")


def display_antonyms(tree):
    '''prints the antonyms for a given word'''

    ant_outer_div = tree.find("div", {"class": "card-box small-box related-box end"})
    if ant_outer_div:
        ant_inner_div = ant_outer_div.find("div", {"class": "definition-block"})
        antonyms = ant_inner_div.get_text()
        print_heading('ANTONYM', Fore.RED)
        print(antonyms[antonyms.find("Antonyms") + len("Antonyms "): antonyms.find("Related Words")])
    else:
        print_error_messages("Ohh! There are no antonyms.")


def words_trending_now(tree):
    '''prints the trending words on Merriam Webster'''

    trending_words = tree.find("div", {"class": "wgt-wap-home-trending-items"})
    if trending_words:
        print_heading('TRENDING WORDS', Fore.BLUE)
        for idx, each in enumerate(trending_words.find_all("li"), 1):
            word = each.find("p", {"class": "title"}).get_text().strip()
            desc = each.find("p", {"class": "blurb"}).get_text().strip()
            print(Fore.RED + str(idx) + ' ' + word + Fore.RESET + ' --> ' + Fore.YELLOW + desc + Fore.RESET)


def word_of_the_day(tree):
    '''prints the word of the day from Merriam Webster'''
    word_of_day = tree.find("div", {"class": "wgt-wod-home"})
    if word_of_day:
        print_heading('WORD OF THE DAY', Fore.BLUE)
        word = word_of_day.find("h4", {"class": "wh-word"}).get_text().strip()
        meaning = word_of_day.find("p", {"class": "wh-def-text"}).get_text().strip()
        print(Fore.GREEN + word.upper() + Fore.RESET + ' : ' + Fore.YELLOW + meaning + Fore.RESET)
        print("")


def get_suggestions(tree):
    '''lists the suggestions for a word in case of 404'''

    suggestions = tree.find_all("p", {"class": "definition-inner-item with-sense"})
    if suggestions:
        print("")
        print(Fore.BLUE + 'It seems that you have not entered a valid word. We know' + Fore.RESET +
              Fore.GREEN + ' To err is human.' + Fore.RESET + Fore.BLUE + ' Hence the suggestions.' + Fore.RESET)
        print_heading('SUGGESTION', Fore.YELLOW)
        print(', '.join([each.get_text() for each in suggestions[0].find_all("a")]))


def make_tree(word, print_meaning=False, print_sentence=False, print_synonym=False, print_antonym=False):
    '''reads the web page and make a html tree'''

    is_error, suggestions_found = [False]*2

    try:
        req = requests.get(BASE_URL.format(word=word), timeout=5)
        if req.status_code == 404:
            suggestions_found = True
    except Exception as e:
        is_error = True
    if not is_error:
        tree = BeautifulSoup(req.text, 'html.parser')
        if req.status_code == requests.codes.ok:
            if print_meaning:
                find_meaning(tree, word)
            if print_sentence:
                display_sentences(tree, word)
            if print_synonym:
                display_synonyms(tree)
            if print_antonym:
                display_antonyms(tree)
        elif suggestions_found:
            if 'spelling suggestion below' in req.text:
                get_suggestions(tree)
            else:
                print_error_messages("The word you've entered was not found. Please try your search again.")
    else:
        print_error_messages("Unable to retrieve meaning. Try again later!")
        sys.exit()


def make_tree_home_page(trending_now=False, word_of_day=False):

    try:
        response = requests.get(HOME_PAGE_URL)
    except Exception as e:
        response = None

    if response and response.status_code == requests.codes.ok:
        tree = BeautifulSoup(response.text, 'html.parser')
        if trending_now:
            words_trending_now(tree)
        if word_of_day:
            word_of_the_day(tree)


def main():
    '''greb is a command line tool to find meanings'''

    arguments = docopt(__doc__, version=__version__)
    if arguments.get('-d') or arguments.get('--rdm'):
        get_meaning_for_terminal()
    elif arguments.get('-t') or arguments.get('--trn'):
        make_tree_home_page(trending_now=True)
    elif arguments.get('-w') or arguments.get('--wrd'):
        make_tree_home_page(word_of_day=True)
    elif arguments['<WORD>']:
        flag_meaning = True
        if (arguments.get('-l') or arguments.get('--all')):
            flag_sentence, flag_synonym, flag_antonym = [True]*3
        else:
            flag_sentence = (arguments.get('-e') or arguments.get('--sen')) or False
            flag_synonym = (arguments.get('-y') or arguments.get('--syn')) or False
            flag_antonym = (arguments.get('-n') or arguments.get('--ant')) or False
        make_tree(arguments['<WORD>'].lower().strip(), print_meaning=flag_meaning,
                  print_sentence=flag_sentence, print_synonym=flag_synonym,
                  print_antonym=flag_antonym)
    else:
        print(__doc__)

if __name__ == '__main__':
    main()
