import macropy.activate     # sets up macro import hooks
import parser                # imports other.py and passes it through import hooks
import test
from eval import compile as c
import eval

print eval.GlobalEnviroment._mapping
print c("(define a 12)", 0)
print c("(if 3 13)", 0)
print c("(defun f (a b c) a)", 0)
print c("""(define a 12)
(print_num a)
""")