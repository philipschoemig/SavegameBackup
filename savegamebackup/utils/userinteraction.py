'''
Created on 22.01.2016

@author: Philip Schoemig
'''
import logging

try:
    import readline
except ImportError:
    import pyreadline as readline


class InputHelper(object):

    def __new__(cls, *p, **k):
        # Ensure the instance is only created once (Singleton)
        if '_the_instance' not in cls.__dict__:
            cls._the_instance = object.__new__(cls)
        return cls._the_instance

    def choice(self, message, options, default=None):
        if len(options) == 0:
            raise ValueError('Options may not be empty')
        if default and default not in options:
            raise ValueError('Default must be included in options')

        options_list = [opt.lower() for opt in options]
        if default:
            default_index = options_list.index(default)
            if default.isalpha():
                options_list[default_index] = default.upper()
            else:
                options_list[default_index] = '{0}*'.format(default)
        options_string = '/'.join(options_list)

        prompt = '{0} [{1}] '.format(message, options_string)
        char = None
        while char not in options:
            char = input(prompt).strip().lower()
            if default and not char:
                char = default
            elif char not in options:
                print('Please enter a valid option.')
        return char

    def confirm(self, message, default=False):
        choice_default = 'n'
        if default:
            choice_default = 'y'
        char = self.choice(message, ['y', 'n'], choice_default)
        if char == 'y':
            return True
        return False

    def select(self, message, iterable):
        if len(iterable) == 1:
            return 0

        options = []
        for index, item in enumerate(iterable):
            options.append(str(index))
            print("{0}. {1}".format(index, item))
        char = self.choice(message, options)
        return int(char)

    def input(self, message, completion_options=None, show_hint=True):
        hint = ''
        if completion_options:
            if show_hint:
                hint = ' (TAB for completion)'
            # Register our completer function
            readline.set_completer(
                SimpleCompleter(completion_options).complete)
            # Use the tab key for completion
            readline.parse_and_bind('tab: complete')

        prompt = "{0}{1}: ".format(message, hint)
        return input(prompt)


class SimpleCompleter(object):

    def __init__(self, options):
        self.options = sorted(options)
        self.matches = None

    def complete(self, text, state):
        response = None
        if state == 0:
            # This is the first time for this text, so build a match list.
            if text:
                self.matches = [s
                                for s in self.options
                                if s and s.startswith(text)]
                #logging.debug('%s matches: %s', repr(text), self.matches)
            else:
                self.matches = self.options[:]
                #logging.debug('(empty input) matches: %s', self.matches)

        # Return the state'th item from the match list,
        # if we have that many.
        try:
            response = self.matches[state]
        except IndexError:
            response = None
        #logging.debug('complete(%s, %s) => %s',
        #              repr(text), state, repr(response))
        return response
