COMMON = {
    'URLS': {
        'base': 'http://www.merriam-webster.com/dictionary/{word}',
        'home': 'http://www.merriam-webster.com',
    },
    'STATUS_CODE': {
        'ok': 200,
        'not-found': 404,
    }
}

READ_PAGE_DATA = [{'url': 'http://www.merriam-webster.com/dictionary/exuberant', 'status_code': 200},
                  {'url': 'http://www.merriam-webster.com/dictionary/asdf', 'status_code': 404},
                  {'url': 'http://www.merriam-.com/dictionary/', 'status_code': False}]


INPUT_WORDS = {
    'MEANING': {
        'awesome': [u': causing feelings of fear and wonder : causing feelings of awe',
                    u': extremely good'],
        'grok': [u': to understand profoundly and intuitively'],
        'recursion': [u'1 : return 1',
                      u'2 : the determination of a succession of elements (as numbers or functions) '
                      'by operation on one or more preceding elements according to a rule or formula '
                      'involving a finite number of steps',
                      u'3 : a computer programming technique involving the use of a procedure, subroutine, '
                      'function, or algorithm that calls itself one or more times until a specified '
                      'condition is met at which time the rest of each repetition is processed from the '
                      'last one called to the first   compare iteration'],
        'darn': [u'1 : to mend with interlacing stitches',
                 u'2 : to embroider by filling in with long running or interlacing stitches',
                 u': to do darning'],
    },
    'SENTENCE': {
        'multitasking': [u'\x1b[36m1. \x1b[39mThe job requires someone who is good at \x1b[36mmultitasking\x1b[39m.'],
        'dimed': [],
    },
    'ANTONYM': {
        'awesome': [u'atrocious, awful, execrable, lousy, pathetic, poor, rotten, terrible, vile, wretched'],
        'dimed': [],
    },
    'SYNONYM': {
        'awesome': [u'amazing, astonishing, astounding, marvelous, awful, eye-opening, fabulous, miraculous, '
                    'portentous, prodigious, staggering, stunning, stupendous, sublime, surprising, wonderful, '
                    'wondrous'],
        'dimed': [],
    }
}

MISSPELLED_WORDS = {
    'asdf': {
        'status_code': 404,
        'suggestion_string': 'spelling suggestion below',
        'suggestion_key': 'suggestion',
        'suggestions': [u'staff, sod off, scoff, scuff, skiff, stiff, stuff, STV, ISDN, Setif, ASTM, stave, '
                        'setoff, Staffa, Pskov, staph, sclaff, skive, stove, stuffy']
    }
}

PRINT_FUNCTION = {
    'print_heading': {
        'input': 'PRINT HEADING FOR TEST',
        'output': '\n\x1b[37mPRINT HEADING FOR TEST\x1b[39m\n\n'
    },
    'print_word': {
         'input': 'awesome',
         'output': '\n##########################\n#        AWESOME         #\n##########################\n'
    },
    'print_error_messages': {
          'input': 'ERROR MESSAGE',
          'output': '\x1b[31mERROR MESSAGE\x1b[39m\n\n'
    },
    'print_result_for_error_msg': {
          'input': '',
          'output': '\x1b[31mOhh! There is no value for erroneous_key.\x1b[39m\n\n'
    },
    'print_result_for_info_msg': {
          'input': 'This is just an info message',
          'output': 'This is just an info message\n'
    },

}
