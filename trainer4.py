#!/usr/bin/env python3

import json, sys, random, datetime


if __name__ == '__main__':

    # Loading config
    with open('config.json', 'r') as myfile:
        data=myfile.read()
    _config = json.loads(data)

    def waiting_for_char(scr, key = "\n"):
        while scr.getkey() != key:
            pass
        return

    def select_from_array(scr, heading, arr):
        '''Select from (id, string)'''
        def fmt(tpl):
            return "{0} {1:.30s}".format(*tpl)

        scr.clear()
        pos = 0

        scr.addstr(1, 1, heading)

        selected = False
        while not selected:
            scr.addstr(3, 1, "Selected {0}/{1}".format(pos+1, len(arr)))
            scr.addstr(5, 1, "-> " + fmt(arr[pos]) + " <-")

            c = scr.getkey()
            if c == 'KEY_UP':
                pos -= 1
                if pos < 0:
                    pos = 0
            elif c == 'KEY_DOWN':
                pos += 1
                if pos >= len(arr):
                    pos = len(arr)-1
            elif c == "\n":
                selected = True
            elif c == 'q':
                return False
        return pos


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

        def learn(self, scr):
            '''Selecting and learning'''
            lsn = self._lessons[select_from_array(scr, "LESSON", [(l._name, '---') for l in self._lessons])]
            lsn.learn(scr)

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

        def learn(self, scr):
            scr.clear()
            st = self.get_exercise_set()
            st.learn(scr)


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

        def learn(self, scr):
            scr.clear()
            lsn = self.get_lesson(15, 1)
            lsn.learn(scr)

    class ExerciseLesson:

        '''One lesson (string) to exercise.'''        

        def __init__(self, ref):
            self._ref = ref
            self._syms = []
            self._typed = ''
            self._started = False
            self._finished = False

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

        def _count_errors(self):
            err = 0
            for i in range(0, len(self._typed)):
                if self._syms[i]._name != self._typed[i]:
                    err += 1
            return err

        def screen(self):
            '''Return Screen'''
            s = Screen()
            s.addstr(5, 1, self.string())
            s.addstr(6, 1, self._typed)

            if self._is_finished():
                s.addstr(8, 1, "Errors: {0}".format(self._count_errors()))
                d = self._finished - self._started
                s.addstr(9, 1, "Time: {0:.2f}".format(d / datetime.timedelta(seconds=1)))

            return s

        def type(self, char):
            '''Typing one char'''
            if len(self._typed) == 0:
                self._started = datetime.datetime.now()
            self._typed += char
            if len(self._typed) == len(self._syms):
                self._finished = datetime.datetime.now()


        def _is_finished(self):
            return len(self._typed) == len(self._syms)

        def learn(self, scr):
            '''All the things to learn'''
            scr.clear()
            self.screen().show(scr)
            while not self._is_finished():
                c = scr.getkey()
                self.type(c)
                self.screen().show(scr)
            waiting_for_char(scr)
            return

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
    # print(qwerty._lessons[1].info())
    ex_set = qwerty._lessons[1].get_exercise_set()
    ex_lesson = ex_set.get_lesson(_config['learning']['string']['length'], 1)
    # print(ex_lesson.string())
    # card = ex_lesson.card()
    # print(card.pretty())

    class Screen:

        def __init__(self):
            self._strings = []

        def addstr(self, y, x, string):
            self._strings.append((y, x, string))

        def show(self, scr, cursor = False):
            for s in self._strings:
                scr.addstr(*s)
            if cursor:
                scr.addstr(cursor, '')

    def main(scr):
        scr.clear()

        layouts = []
        for l in _config['layouts']:
            layouts.append((l['hotkey'], l['name']))
        layout = _config['layouts'][select_from_array(scr, "LAYOUT", layouts)]
        if not layout:
            sys.exit(0)

        training_layout = Layout(layout['name'],
                                 layout['hotkey'],
                                 layout['symbols'],
                                 layout['lessons'])

        training_layout.learn(scr)


        

    import curses
    from curses import wrapper

    wrapper(main)
