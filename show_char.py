#!/usr/bin/env python3

if __name__ == '__main__':

    # Loading config

    def main(scr):
        scr.clear()
        while True:
            c = scr.getkey()
            scr.addstr(1, 1, '    ')
            scr.addstr(1, 1, c)

    import curses
    from curses import wrapper

    wrapper(main)
