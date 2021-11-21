#!/usr/bin/env python3

import json

if __name__ == '__main__':

    # Loading config
    with open('config.json', 'r') as myfile:
        data=myfile.read()
    _config = json.loads(data)

    class Pos:

        _diffs = _config['keyboard']['difficulties']

        def __init__(self, pos):
            self._pos = pos

        def diff(self):
            d = 1
            for p in self._pos:
                d *= self._diffs[p][self._pos[p]]
            return d

    class Symbol:

        def __init__(self, s):
            self._name = s['symbol']
            self._classes = s['classes']
            self._pos = Pos(s['position'])

        def info(self):
            return "{0} {1:.2f}".format(self._name, self._pos.diff())

    class Layout:

        def __init__(self, name, hotkey, symbols):
            self._name = name
            self._hotkey = hotkey
            self._symbols = []
            for s in symbols:
                self._symbols.append(Symbol(s))

        def symbols(self):
            report = []
            for s in self._symbols:
                report.append(s.info())
            return "\n".join(report)

    l = _config['layouts'][0]
    qwerty = Layout(l['name'], l['hotkey'], l['symbols'])

    print(qwerty.symbols())
