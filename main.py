import macropy.activate     # sets up macro import hooks
import parser                # imports other.py and passes it through import hooks
import test
from eval import compile as c
import eval

# print eval.GlobalEnviroment._mapping
# print c("(define a 12)", 0)
# print c("(defun f (a b c) a)", 0)
# print c("""(print_num (+ 1 2 3))
# """)

# print c("""
# (> 3 2)
# """)

import sys
print c(open(sys.argv[1]).read(), 3)