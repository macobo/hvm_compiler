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
        self.assertEqual(i(-660), -660)

class Enviroments(unittest.TestCase):
    def test_env(self):
        A = Enviroment.Local(Enviroment.Nil)
        B = Enviroment.Local(A)
        A.set("key",2)
        self.assertEqual(B.get("key"), 2)
        B.set("key", 5)
        self.assertEqual(B.get("key"), 5)
        self.assertEqual(A.get("key"), 2)


for k in [Parsing, Enviroments]:
    suite = unittest.TestLoader().loadTestsFromTestCase(k)
    unittest.TextTestRunner(verbosity=2).run(suite)