EGG_FILENAME = r"C:\Program Files (x86)\JetBrains\PyCharm 2016.3.1\debug-eggs\pycharm-debug.egg"
HOST = 'localhost'
PORT = 4434

import sys
if EGG_FILENAME not in sys.path:
    sys.path.append(EGG_FILENAME)

import pydevd
pydevd.settrace(HOST, port=PORT, stdoutToServer=True, stderrToServer=True)
