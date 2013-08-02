import macropy.activate     # sets up macro import hooks
import unittest

from eval import *
from parser import *

from helpers import evaluate_number

class Parsing(unittest.TestCase):
    def test_expr_parsing(self):
        target = List([
            List([Number(1)]), 
            Number(2),
            Symbol("helloWorld"),
            Number(-3),
            List([])
        ])
        self.assertEqual(expr.parse("((1) 2 helloWorld -3 ())"), target)

    def test_program_parsing(self):
        target = [
            List([Symbol("define"), Symbol("a"), Number(12)]),
            List([Symbol("print_num"), Symbol("a")])
        ]
        self.assertEqual(program_parser.parse("""(define a 12)
(print_num a)
"""), target)

    def test_numbers(self):
        c = lambda n: Number(n).compile({})
        i = lambda n: evaluate_number(c(n))[0]

        self.assertEqual(c(0), "0")
        self.assertEqual(c(8), "8")
        self.assertEqual(c(9), "9")
        self.assertEqual(i(28), 28)
        self.assertEqual(i(-10), -10)
        self.assertEqual(i(-6660), -6660)


suite = unittest.TestLoader().loadTestsFromTestCase(Parsing)
unittest.TextTestRunner(verbosity=2).run(suite)