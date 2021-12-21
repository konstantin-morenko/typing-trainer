#!/usr/bin/env python3

import json
import sys

import curses
from curses import wrapper

class Symbol:

    def __init__(self, o, diff):
        self._sym = o['symbol']
        self._cls = o['classes']
        self._pos = o['position']
        self._diff = diff

    def diff(self):
        d = 1
        for p in self._pos:
            d *= self._diff[p][self._pos[p]]
        return d

    def __str__(self):
        return self._sym


def menu_main(scr):
    while True:

        scr.clear()

        scr.addstr(2, 1, '========== MAIN MENU ==========')
        scr.addstr(4, 1, '(t) Training')
        scr.addstr(8, 1, '(q) Exit')

        k = scr.getkey()

        if k == 'q':
            sys.exit()
        elif k == 't':
            menu_layout(scr)


def menu_layout(scr):

    while True:

        scr.clear()

        scr.addstr(2, 1, 'LAYOUT MENU')
        scr.addstr(4, 1, '(q) Back')

        for i in range(0, len(_config['layouts'])):
            layout = _config['layouts'][i]
            scr.addstr(i+6, 1, '(' + layout['hotkey'] + ') ' + layout['name'])

        k = scr.getkey()
        if k == 'q':
            return
        else:
            for l in _config['layouts']:
                if k == l['hotkey']:
                    menu_type(scr, l)


def menu_type(scr, layout):

    while True:

        scr.clear()

        scr.addstr(2, 1, 'TRAIN TYPE MENU')
        scr.addstr(4, 1, '(q) Back')

        scr.addstr(6, 1, '(c) Course')

        k = scr.getkey()
        if k == 'q':
            return
        elif k == 'c':
            menu_course_selection(scr, layout)

def menu_course_selection(scr, layout):

    while True:

        scr.clear()

        scr.addstr(2, 1, 'COURSE SELECTION')
        scr.addstr(4, 1, '(q) Back')

        courses = layout['courses']
        for i in range(0, len(courses)):
            scr.addstr(i+6, 1, str(i) + ' ' + courses[i]['name'])

        curses.echo()
        c = ''
        course = ''
        while c != '\n':
            if c == 'q':
                return
            course += c
            c = stdscr.getkey()

        curses.noecho()
        menu_course_type(scr, layout, course)

def menu_course_type(scr, layout, course):

    while True:

        scr.clear()

        scr.addstr(2, 1, 'COURSE TYPE')
        scr.addstr(4, 1, '(q) Back')

        scr.addstr(6, 1, '(n) Only new')
        scr.addstr(7, 1, '(f) Full')

        k = scr.getkey()
        if k == 'q':
            return
        elif k == 'n':
            training_layout = mk_layout(layout, int(course), True)
            trainer(scr, training_layout)
        elif k == 'f':
            pass

def mk_layout(layout, course, only_new):
    # Preparing letters
    l = []
    l = layout['courses'][course]['new']
    # Preparing array
    d = []
    s = layout['symbols']
    for i in l:
        for j in layout['symbols']:
            if j['symbol'] == i:
                d.append(j)
    return j

def trainer(scr, layout):
    lesson = gen(layout)

    stdscr.clear()

    start = None
    end = None
    errors = 0
    pos = 0
    
    while(pos < len(lesson)):
        stdscr.addstr(5, 1, lesson)
        stdscr.addstr(6, 1+pos, '')

        stdscr.refresh()
        c = stdscr.getkey()

        if c == '\n':
            end = datetime.datetime.now()
            break

        # stdscr.addstr(12, 1, 'Key: ' + str(c))

        if(c == lesson[pos]):
            pair = 2
        else:
            pair = 1
            errors += 1
            
        stdscr.attron(curses.A_REVERSE | 
                curses.color_pair(pair))
        stdscr.addstr(6, 1+pos, c)
        stdscr.attroff(curses.A_REVERSE |
                 curses.color_pair(pair))

        pos += 1
        if pos == 1:
            start = datetime.datetime.now()
        if pos == len(lesson):
            end = datetime.datetime.now()

    stdscr.addstr(8, 1, 'Errors: ' + str(errors))

    delta = end - start
    time = int((delta / datetime.timedelta(microseconds=1)) / 1e6)
    stdscr.addstr(9, 1, 'Time: ' + str(time) + ' s')

    cpm = int((pos / time) * 60)
    stdscr.addstr(10, 1, 'CPM: ' + str(cpm) + ' cpm')

    score = int(diff * pos * (cpm / 120))
    stdscr.addstr(11, 1, 'Score: ' + str(score))

    # Any key to exit
    c = stdscr.getkey()

def gen(syms, l = 60, d = False):
    s = ''
    diff = 0
    if not d:
        d = (min(list(syms.values())) + max(list(syms.values()))) / 2
    for i in range(1, l):
        k = list(syms.keys())
        if avr_diff(s) > d:
            w = 500
            while w > d:
                c = random.choice(k)
                w = syms[c]
        else:
            w = -500
            while w < d:
                c = random.choice(k)
                w = syms[c]
        s += c
    return s






def main(stdscr):
    stdscr.clear()
    menu_main(stdscr)
    


with open('config.json', 'r') as myfile:
    data=myfile.read()
_config = json.loads(data)

stdscr = curses.initscr()

wrapper(main)
