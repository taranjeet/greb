COMMON = {
    'URLS': {
        'base': 'http://www.merriam-webster.com/dictionary/{word}',
        'home': 'http://www.merriam-webster.com',
        'invalid': 'http://www.merriam-.com/dictionary/',
    },
    'STATUS_CODE' : {
        'ok': 200,
        'not-found': 404,
    }
}

READ_PAGE_DATA = {
    'exuberant': 200,
    'asdf': 404,
}

INPUT_WORDS = {
    'MEANING': {
        'awesome': [': causing feelings of fear and wonder : causing feelings of awe',
                    ': extremely good',],
        'grok': [': to understand profoundly and intuitively',],
        'recursion': ['1 : return 1',
                      '2 : the determination of a succession of elements (as numbers or functions) '
                      'by operation on one or more preceding elements according to a rule or formula '
                      'involving a finite number of steps',
                      '3 : a computer programming technique involving the use of a procedure, subroutine, '
                      'function, or algorithm that calls itself one or more times until a specified '
                      'condition is met at which time the rest of each repetition is processed from the '
                      'last one called to the first   compare iteration',],
        'darn': ['1 : to mend with interlacing stitches',
                 '2 : to embroider by filling in with long running or interlacing stitches',
                 ': to do darning',],
    },
    'SENTENCE': {
        'multitasking': ['\x1b[36m1. \x1b[39mThe job requires someone who is good at \x1b[36mmultitasking\x1b[39m.'],
        'dimed': [],
    },
    'ANTONYM': {
        'awesome': ['atrocious, awful, execrable, lousy, pathetic, poor, rotten, terrible, vile, wretched'],
        'dimed': [],
    },
    'SYNONYM': {
        'awesome': ['amazing, astonishing, astounding, marvelous, awful, eye-opening, fabulous, miraculous, '
        'portentous, prodigious, staggering, stunning, stupendous, sublime, surprising, wonderful, wondrous'],
        'dimed': [],
    }
}
