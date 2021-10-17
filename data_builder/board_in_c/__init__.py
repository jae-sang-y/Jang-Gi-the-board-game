import ctypes as c
import os

print(os.path.join(os.getcwd(), r'board_in_c\board_in_c.dll'))
_bic = c.windll.LoadLibrary(os.path.join(os.getcwd(), r'board_in_c\board_in_c.dll'))

_bic.init()
get_str = _bic.get_str
get_str.restype = c.py_object
