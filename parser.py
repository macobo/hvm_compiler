from macropy.peg import macros, peg, cut
from macropy.quick_lambda import macros, f
from macropy.case_classes import macros, case

@case
class Symbol(value): pass

@case
class Label(value): 
    def compile(self, env):
        env.set(self, env.compile_position)

@case
class Number(value):
    def compile(self, env = None):
        if self.value < 0:
            return "0" + Number(-self.value).compile(env) + "-"
        return fastest(self.value)

@case
class Command(name, args | None): 
    if self.args is None: 
        self.args = []

    def compile(self, env):
        function = env.get(name)
        return function(*args)


# lisp grammar

with peg:
    space = '\s*'.r

    symbol = '[0-9a-zA-Z-?!*+/><=_]+'.r // Symbol
    number = '-?[0-9]+'.r  // int
    label  = (symbol is s, ':') >> Label(s.value)
    string = ('"', '[^"]*'.r, '"') // f[_[1]]

    expr = number | symbol | string

    comment = '[^\n]*//[^\n]*\n'.r >> []

    separators = (comment | space).rep

    command = (symbol is name, space, expr.rep_with(space) is args, ';') >> Command(name, args)
    program = (space, (comment | command | label).rep_with(space), space) // f[_[1]]


def parse_program(asm_text):
    list_of_commands = program.parse(asm_text)
    return filter(lambda x: x, list_of_commands)