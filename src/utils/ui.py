'''
Created on 22.01.2016

@author: Philip Schoemig
'''


class UserInteraction(object):

    @staticmethod
    def choice(message, options, default=None):
        prompt = '{0} ({1}) [{2}]: '.format(
            message, ','.join(options), default)
        char = None
        while char not in options:
            char = raw_input(prompt).strip().lower()
            if default and not char:
                char = default
            elif char not in options:
                print 'Please enter a valid option.'
        return char

    @staticmethod
    def confirm(message, default=False):
        choice_default = 'n'
        if default:
            choice_default = 'y'
        char = UserInteraction.choice(message, ['y', 'n'], choice_default)
        if not char:
            return default
        if char == 'y':
            return True
        return False

    @staticmethod
    def select(message, iterable):
        if len(iterable) == 1:
            return 0

        options = []
        for index, item in enumerate(iterable):
            options.append(str(index))
            print "{0}. {1}".format(index, item)
        char = UserInteraction.choice(message, options)
        return int(char)
