import macropy.activate     # sets up macro import hooks
import parser                # imports other.py and passes it through import hooks
import test
from eval import compiler as c
import eval
import os

# print eval.GlobalEnviroment._mapping
# print c("(define a 12)", 0)
# print c("(defun f (a b c) a)", 0)
# print c("""(print_num (+ 1 2 3))
# """)

# print c("""
# (> 3 2)
# """)

print c("(block 1 2 3 4)")

import sys
if len(sys.argv) > 1:
    result = c(open(sys.argv[1]).read(), 300)
    print
    print result
    os.popen('xclip -selection c', 'w').write(result)