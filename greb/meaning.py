r"""

Findmeaning is a command line tool to find meaning of words.

Usage: findmeaning <WORD> [-leyn] [-h | --help]

Options:
    -l --all        Lists everything
    -e --sen        Lists sentence
    -y --syn        Lists synonyms
    -n --ant        Lists antonyms
    --version       Lists version
    -h --help       Lists help
"""

import requests
import sys
from bs4 import BeautifulSoup
from colorama import Fore
from docopt import docopt

__version__ = '0.0.3'

BASE_URL = 'http://www.merriam-webster.com/dictionary/'

requests.packages.urllib3.disable_warnings()


def print_heading(heading, color):
    '''prints the heading for a section of output'''
    print("")
    print(color + heading + Fore.RESET)
    print("")


def print_error_messages(msg):
    '''prints the error messgaes in red'''
    print(Fore.RED + msg + Fore.RESET)


def display_meaning(tree):
    '''prints the meaning corresponding to a word'''
    meanings = tree.find("div", {"class": "ld_on_collegiate"})
    found_meaning = False
    if meanings:
        found_meaning = True
        print_heading('MEANING', Fore.YELLOW)
        for each in meanings.findAll("p"):
            print(each.text)
    else:
        meanings = tree.find("span", {"class": "ssens"})
        if meanings:
            found_meaning = True
            print_heading('MEANING', Fore.YELLOW)
            for each in meanings.text.split(':'):
                if len(each.strip()) > 0:
                    print(': ' + each)
    if not found_meaning:
        print_error_messages("Unable to find meaning for this word. Are you sure its spelled right?")


def display_sentences(tree, word):
    '''prints the sentences showing the use of a word'''
    sentences = tree.find("div", {"class": "example-sentences"})
    if sentences:
        print_heading('SENTENCE', Fore.GREEN)
        for each in sentences.findAll("li", {"class": "always-visible"}):
            print(each.text.replace(word, Fore.CYAN + word + Fore.RESET))
    else:
        print_error_messages("Oops! There are no sentences to display. Why not frame your own?")


def display_synonyms(tree):
    '''prints the synonyms for a given word'''
    synonyms = tree.find("dl")
    if synonyms:
        print_heading('SYNONYM', Fore.BLUE)
        print(', '.join([each.text for each in synonyms.findAll("a")]))
    else:
        print_error_messages("Ohh! There are no synonyms.")


def display_antonyms(tree):
    '''prints the antonyms for a given word'''
    antonyms = tree.findAll("dl")
    if len(antonyms) > 1:
        antonyms = antonyms[1]
        print_heading('ANTONYM', Fore.RED)
        print(', '.join([each.text for each in antonyms.findAll("a")]))
    else:
        print_error_messages("Ohh! There are no antonyms.")


def make_tree(word, print_meaning=False, print_sentence=False, print_synonym=False, print_antonym=False):
    '''reads the web page and make a html tree'''
    req = requests.get(BASE_URL+word)
    if req.status_code == requests.codes.ok:
        tree = BeautifulSoup(req.text, 'html.parser')
        if print_meaning:
            display_meaning(tree)
        if print_sentence:
            display_sentences(tree, word)
        if print_synonym:
            display_synonyms(tree)
        if print_antonym:
            display_antonyms(tree)
    else:
        print_error_messages("Unable to retrieve meaning. Try again later!")
        sys.exit()


def main():
    '''findmeaning is a command line tool to find meanings'''
    arguments = docopt(__doc__, version=__version__)
    if arguments['<WORD>']:
        flag_meaning = True
        if (arguments.get('-l') or arguments.get('--all')):
            flag_sentence, flag_synonym, flag_antonym = [True]*3
        else:
            flag_sentence = (arguments.get('-e') or arguments.get('--sen')) or False
            flag_synonym = (arguments.get('-y') or arguments.get('--syn')) or False
            flag_antonym = (arguments.get('-n') or arguments.get('--ant')) or False
        make_tree(arguments['<WORD>'].lower(), print_meaning=flag_meaning,
                  print_sentence=flag_sentence, print_synonym=flag_synonym,
                  print_antonym=flag_antonym)
    else:
        print(__doc__)

if __name__ == '__main__':
    main()
