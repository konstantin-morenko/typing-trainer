#!/usr/bin/env python3

def train(screen, string):

    screen.addstr(2, 1, '---------- TRAINING ----------')

    for i in range(0, len(string)):
        screen.addstr(4, 1+i, string[i].char())

    pos = 0
    state = 'started'

    while state != 'ended':
        c = screen.getkey()

        if c == '\n':
            state = 'ended'
            break
        else:
            char = c

        if string[pos].char() == c:
            p = c
        else:
            p = '*'
        screen.addstr(5, 1+pos, p)

        pos += 1

        if pos == len(string):
            state = 'ended'
            break

    screen.addstr(7, 1, 'Ended')
    screen.getkey()

class Char:

    def __init__(self, char):
        self._char = char

    def char(self):
        return self._char

if __name__ == '__main__':

    import curses
    from curses import wrapper

    import json

    def main(stdscr):
        stdscr.clear()
        a = Char('a')
        b = Char('b')
        c = Char('c')
        s = [a, b, c, b, c, a, c, a, b]
        train(stdscr, s)


    with open('config.json', 'r') as myfile:
        data=myfile.read()
    _config = json.loads(data)

    stdscr = curses.initscr()

    wrapper(main)
