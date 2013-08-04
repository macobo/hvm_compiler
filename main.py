import macropy.activate     # sets up macro import hooks
import parser                # imports other.py and passes it through import hooks
import test
from eval import compiler
import eval
import os

def c(string):
    result = compiler(string)
    os.popen('xclip -selection c', 'w').write(result)
    print
    return result

print c("""
(defun recursion (a)
    (print_string "beginning recursion ")
    (print_num a)
    (print_string "\n")
    (if (<= a 3)
        (recursion (+ a 1)))
    (print_string "ending recursion ")
    (print_num a)
    (print_string "\n"))
(recursion 0)
""")

print c("""
(SetMemoryStart 0)
(define x 0)
(do_while (<= x 3) 
    (print_num x)
    (define x (+ x 1)))
""")

print c("""
(or 1 0)
""")

import sys
if len(sys.argv) > 1:
    result = c(open(sys.argv[1]).read())
    print result
    if len(sys.argv) == 3:
        open(sys.argv[2], "w").write(result)