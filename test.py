import macropy.activate     # sets up macro import hooks
import unittest

from parser import *

from helpers import evaluate_number

class Parsing(unittest.TestCase):
    def test_program_parsing(self):
        expected = [
            Label("beginning"),
            Command(Symbol("hello"), [Symbol("world"), Number(1), Number(2), Number(3)]),
            Command(Symbol("blah"), [])
        ]
        self.assertEqual(expected, parse_program("""
beginning:
    hello world 1 2 3;
    // some comment
    blah;
"""))

    def test_command_parsing(self):
        target = Command(Symbol("hello"), [
            Symbol("world"),
            Number(1),
            Number(2),
            Number(-3)
        ])
        self.assertEqual(command.parse("hello world 1 2 -3;"), target)
        

    def test_string(self):
        target = "Hello!"
        self.assertEqual(string.parse('"Hello!"'), target)


    def test_numbers(self):
        c = lambda n: Number(n).compile({})
        i = lambda n: evaluate_number(c(n))[0]

        self.assertEqual(c(0), "0")
        self.assertEqual(c(8), "8")
        self.assertEqual(c(9), "9")
        self.assertEqual(i(28), 28)
        self.assertEqual(i(-10), -10)
        self.assertEqual(i(-660), -660)


for k in [Parsing]:
    suite = unittest.TestLoader().loadTestsFromTestCase(k)
    unittest.TextTestRunner(verbosity=2).run(suite)