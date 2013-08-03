from macropy.peg import macros, peg, cut
from macropy.quick_lambda import macros, f
from macropy.tracing import macros, require

from eval import Symbol, Number, List

# lisp grammar
with peg:
    space = '\s*'.r
    symbol = '[0-9a-zA-Z-?!*+/><=_]+'.r // Symbol
    number = ('-?[0-9]+'.r is v) >> Number(int(v))
    list = ('(', space, expr.rep_with(space) is e, space, ')') >> List(e)
    string = ('"', '[^"]*'.r, '"') // f[_[1]]
    expr = number | symbol | list | string | comment

    comment = '[^\n]*;[^\n]*\n'.r >> List([])
    program_parser = (space, expr.rep_with(space), space) // f[_[1]]
