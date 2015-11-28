Greb
=====
[![PyPI version](https://badge.fury.io/py/greb.svg)](https://badge.fury.io/py/greb)

This python package finds the meaning for a word. It also lists the sentences,
synonyms and antonyms for a given word. If a word is misspeled, it lists the suggestion 
for that word. Greb stands for Grab meaning from web.

Install
=======

* Using `pip`
```
$ pip install greb
```

* From source

```
$ git clone https://github.com/staranjeet/greb
$ cd greb
$ python setup.py install
```

Usage
=====

```
$ greb awesome

MEANING

: causing feelings of fear and wonder : causing feelings of awe
: extremely good

```

Available Options
=================

```

 -l --all        Lists everything
 -e --sen        Lists sentence
 -y --syn        Lists synonyms
 -n --ant        Lists antonyms
 --help 		 Lists help
 --version       Lists version

```

Licence
====
Open sourced under [MIT License](LICENSE.txt)

Package Link
============

Pypi [link](https://pypi.python.org/pypi/greb)

TODOS
======
[] Replace bs4 functions to follow pep8 standard, like findAll to find_all
