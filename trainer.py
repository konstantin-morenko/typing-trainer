#!/usr/bin/env python3

import curses
from curses import wrapper

import datetime

import random

import sys

import json

HOME=1
UPPER=2
LOWER=4
DIGITS=3
SPACE = 0.5

THUMB=0.2
INDEX=1
MIDDLE=1
RING=1.2
PINKY=1.3

SHIFT=1.5

RIGHT=1
LEFT=1.05

INTERNAL=1.05

syms = {'a':HOME*PINKY*LEFT,
        'b':LOWER*INDEX*RIGHT*INTERNAL,
        'c':LOWER*MIDDLE*LEFT,
        'd':HOME*MIDDLE*LEFT,
        'e':UPPER*MIDDLE*LEFT,
        'f':HOME*INDEX*LEFT,
        'g':HOME*INDEX*LEFT*INTERNAL,
        'h':HOME*INDEX*RIGHT*INTERNAL,
        'i':UPPER*MIDDLE*RIGHT,
        'j':HOME*INDEX*RIGHT,
        'k':HOME*MIDDLE*RIGHT,
        'l':HOME*RING*RIGHT,
        'm':LOWER*INDEX*RIGHT,
        'n':LOWER*INDEX*RIGHT,
        'o':UPPER*RING*RIGHT,
        'p':UPPER*PINKY*RIGHT,
        'q':UPPER*PINKY*LEFT,
        'r':UPPER*INDEX*LEFT,
        's':HOME*RING*LEFT,
        't':UPPER*INDEX*LEFT*INTERNAL,
        'u':UPPER*INDEX*RIGHT*INTERNAL,
        'v':LOWER*INDEX*LEFT,
        'w':UPPER*RING*LEFT,
        'x':LOWER*RING*LEFT,
        'y':UPPER*INDEX*RIGHT,
        'z':LOWER*PINKY*LEFT}

lessons = [{'f': syms['f'], 'j': syms['j']},
           {'f': syms['f'], 'g': syms['g'], 'h': syms['h'], 'j': syms['j']}]

def symbol_diff(pos, diffs):
    d = 1
    for p in pos:
        d *= diffs[p][pos[p]]
    return d

def get_difficulties(syms):
    diffs = []
    for c in list(syms['symbols']):
        d = symbol_diff(c['position'], _config['keyboard']['difficulties'])
        if d not in diffs:
            diffs.append(d)
    diffs.sort()
    return diffs

def select_difficulties(syms, max_diff):
    out = {}
    for c in syms:
        if syms[c] <= max_diff + 0.001:
            out[c] = syms[c]
    return out

def sel_lesson(scr):
    scr.clear()
    # stdscr.addstr(2, 1, "Select lesson (" + str(len(lessons)) + "): ")
    available_diffs = get_difficulties(syms)
    for i in range(0, len(available_diffs)):
        # s = ''.join(list(lessons[i].keys()))
        stdscr.addstr(4+i, 1, str(i) + " " + str(available_diffs[i]) + " " + "".join([x for x in list(select_difficulties(syms, available_diffs[i]).keys())]))

    stdscr.addstr(2, 1, "Select difficulty: ")
    c = ''
    l = ''
    while c != 'KEY_UP':
        l += c
        c = stdscr.getkey()
    return select_difficulties(syms, available_diffs[int(l)])


def avr_diff(s):
    diff = 0
    for c in s:
        diff += syms[c]
    if len(s) == 0:
        return 0
    else:
        return diff / len(s)

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

def menu_main(scr):
    while True:

        scr.clear()

        scr.addstr(2, 1, 'MAIN MENU')

        scr.addstr(4, 1, '(t) Training')
        scr.addstr(5, 1, '( ) Statistics')
        scr.addstr(6, 1, '( ) Highscores')

        scr.addstr(8, 1, '(q) Exit')

        scr.addstr(10, 1, 'HERE WILL BE HIGHSCORES')

        k = scr.getkey()
        if k == 't':
            menu_layout(scr)
        elif k == 'q':
            sys.exit()

def menu_layout(scr):

    while True:

        scr.clear()

        scr.addstr(2, 1, 'LAYOUT MENU')
        scr.addstr(3, 1, '(q) Back')

        for i in range(0, len(_config['layouts'])):
            layout = _config['layouts'][i]
            scr.addstr(i+5, 1, '(' + layout['hotkey'] + ') ' + layout['name'])

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

        scr.addstr(4, 1, '(d) Difficulty')
        scr.addstr(5, 1, '( ) Category')
        scr.addstr(6, 1, '( ) Errors')
        scr.addstr(7, 1, '( ) Individual')

        scr.addstr(9, 1, '(q) Back')

        k = scr.getkey()
        if k == 'd':
            menu_difficulty(scr, layout)
        elif k == 'q':
            return

def menu_difficulty(scr, layout):
    while True:

        scr.clear()

        curses.echo()
        
        available_diffs = get_difficulties(layout)
        for i in range(0, len(available_diffs)):
            stdscr.addstr(4+i, 1, str(i) + " " + str(available_diffs[i]))

        stdscr.addstr(2, 1, "Select difficulty: ")
        c = ''
        l = ''
        while c != '\n':
            if c == 'q':
                return
            l += c
            c = stdscr.getkey()

        curses.noecho()
        
        # trainer(scr, select_difficulties(layout, available_diffs[int(l)]))

def trainer(scr, layout):
    lesson = gen(layout)
    diff = avr_diff(lesson)

    stdscr.clear()

    start = None
    end = None
    errors = 0
    pos = 0
    
    stdscr.addstr(2, 1, 'Difficulty: ' + str(diff))

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





def main(stdscr):
    stdscr.clear()

    curses.init_color(1, 255, 0, 0)
    curses.init_color(2, 0, 255, 0)
    curses.init_color(3, 10, 10, 10)

    curses.init_pair(1, 1, 3)
    curses.init_pair(2, 2, 3)

    menu_main(stdscr)
    


with open('config.json', 'r') as myfile:
    data=myfile.read()
_config = json.loads(data)

stdscr = curses.initscr()

wrapper(main)
