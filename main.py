import macropy.activate     # sets up macro import hooks
import parser                # imports other.py and passes it through import hooks
import test
from eval import compiler
import eval
import os

def c(string):
    result = compiler(string)
    os.popen('xclip -selection c', 'w').write(result)
    return result

print c("""(print_string "Hello!\nWorld")""")

import sys
if len(sys.argv) > 1:
    print
    print c(open(sys.argv[1]).read())