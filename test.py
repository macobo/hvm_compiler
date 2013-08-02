import macropy.activate     # sets up macro import hooks
import unittest

from eval import *
from parser import *

class Parsing(unittest.TestCase):
    def test_parsing(self):
        target = List([
            List([Number(1)]), 
            Number(2),
            Symbol("helloWorld"),
            Number(-3),
            List([])
        ])
        self.assertEqual(expr.parse("((1) 2 helloWorld -3 ())"), target)

    def test_numbers(self):
        c = lambda n: Number(n).compile({})
        self.assertEqual(c(0), "0")
        self.assertEqual(c(8), "8")
        self.assertEqual(c(9), "9")
        self.assertEqual(c(28), "999++1+")
        self.assertEqual(c(-10), "091+-")


suite = unittest.TestLoader().loadTestsFromTestCase(Parsing)
unittest.TextTestRunner(verbosity=2).run(suite)