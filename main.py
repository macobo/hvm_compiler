import macropy.activate     # sets up macro import hooks
from parser import *
import test
from pprint import pprint

def copy(what):
    os.popen('xclip -selection c', 'w').write(what)