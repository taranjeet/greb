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

$ greb --rdm 

# fetches a random meaning from searcher history

```

Available Options
=================

```

 -l --all        Lists everything
 -e --sen        Lists sentence
 -y --syn        Lists synonyms
 -n --ant        Lists antonyms
 -d --rdm        Displays a random from searched history
 --help 		 Lists help
 --version       Lists version

```

Additional Usage
================

Greb by default saves all the words searched in a file named `meanings.json` under home directory.
One use of greb can be to display a random word from your searched history whenever a new instance
of terminal is launched. To use it in this way, one needs to configure its `bashrc` and write 
`greb -d` or `greb --rdm` at the end of it.


Todos
=====

[ ] Need to update parsing structure.

[ ] Implementation as a class

[ ] Option to turn off or on display.

License
====
Open sourced under [MIT License](LICENSE.txt)

Package Link
============

Pypi [link](https://pypi.python.org/pypi/greb)
