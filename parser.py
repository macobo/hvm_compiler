from macropy.peg import macros, peg
from macropy.quick_lambda import macros, f
from macropy.tracing import macros, require

from eval import Symbol, Number, List

# lisp grammar
with peg:
    space = '\s*'.r
    symbol = '[0-9a-zA-Z-?!*+/><=_]+'.r // Symbol
    number = ('-?[0-9]+'.r is v) >> Number(int(v))
    list = ('(', (expr is first, (space, expr is rest).rep ).opt, ')') >> List.c(first, rest)
    expr = number | symbol | list
    program_parser = (space, expr.rep_with(space), space) // f[_[1]]
