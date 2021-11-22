#!/usr/bin/env python3

import json
import random


if __name__ == '__main__':

    # Loading config
    with open('config.json', 'r') as myfile:
        data=myfile.read()
    _config = json.loads(data)

    class Pos:

        '''Holding position of a key with difficulties.'''

        _diffs = _config['keyboard']['difficulties']

        def __init__(self, pos):
            self._pos = pos

        def diff(self):
            d = 1
            for p in self._pos:
                d *= self._diffs[p][self._pos[p]]
            return d

    class Symbol:

        '''Separate symbol on the keyboard.'''

        def __init__(self, s):
            self._name = s['symbol']
            self._classes = s['classes']
            self._pos = Pos(s['position'])

        def info(self):
            return "{0} {1:.2f}".format(self._name, self._pos.diff())

    class Layout:

        '''The whole keyboard layout with lessons and courses.'''

        def __init__(self, name, hotkey, symbols, lessons):

            self._name = name
            self._hotkey = hotkey

            self._symbols = []
            for s in symbols:
                self._symbols.append(Symbol(s))

            self._lessons = []
            for l in lessons:
                syms = []
                for s in l['symbols']:
                    syms.append(self._s_sym(s))
                lo = Lesson(l['name'], syms)
                self._lessons.append(lo)

        def _s_sym(self, sym):
            '''Search for particular symbol.'''
            for s in self._symbols:
                if s._name == sym:
                    return s

        def symbols(self):
            '''Print all symbols.'''
            report = []
            for s in self._symbols:
                report.append(s.info())
            return "\n".join(report)

        def lessons(self):
            report = []
            for l in self._lessons:
                report.append(l.info())
            return "\n".join(report)

    class Lesson:

        def __init__(self, name, symbols):
            self._name = name
            self._symbols = symbols

        def info(self):
            sstr = ""
            for s in self._symbols:
                sstr += s._name
            return "{0}: {1}".format(self._name, sstr)

        def get_exercise_set(self):
            return ExerciseSet(self._name, self, self._symbols)

    class ExerciseSet:

        '''Set to generate exercise strings.'''

        def __init__(self, name, ref, symbols):
            self._name = name
            self._ref = ref
            self._symbols = symbols

        def get_lesson(self, length, avr_diff):
            ls = ExerciseLesson(self)
            for i in range(0, length):
                ls.append(random.choice(self._symbols))
            return ls

    class ExerciseLesson:

        '''One lesson (string) to exercise.'''        

        def __init__(self, ref):
            self._ref = ref
            self._syms = []

        def append(self, sym):
            self._syms.append(sym)

        def string(self):
            string = ""
            for s in self._syms:
                string += s._name
            return string

        def card(self):
            c = Card()
            c.append('name', self._ref._name)
            c.append('set', ''.join([x._name for x in self._syms]))
            return c

    class Card:
        '''Card for pretty printing.'''

        def __init__(self):
            self._content = {}

        def append(self, name, value):
            self._content[name] = value

        def pretty(self):
            max_key = max([len(k) for k in self._content])
            max_val = max([len(self._content[k]) for k in self._content])
            s = []
            for k in self._content:
                s.append(("{0:" + str(max_key) + "} : {1}").format(k, self._content[k]))
            return '\n'.join(s)


    class Course:

        '''Course with set of lessons.'''
        # Consists as a set of lessons with new and all symbols
        pass


    l = _config['layouts'][0]
    qwerty = Layout(l['name'], l['hotkey'], l['symbols'], l['lessons'])

    # print(qwerty.symbols())
    print(qwerty._lessons[1].info())
    ex_set = qwerty._lessons[1].get_exercise_set()
    ex_lesson = ex_set.get_lesson(15, 1)
    # print(ex_lesson.string())
    card = ex_lesson.card()
    print(card.pretty())
