from macropy.case_classes import macros, case

from helpers import memoize

@case
class Symbol(value): 
    def compile(self, env):
        return env.get(self).position_get_expr(env)

@case
class List(value): 
    @staticmethod
    def c(first, rest):
        return List([first] + rest if first else [])

    def compile(self, env):
        if not self.value: return ""
        name, args = self.value[0], self.value[1:]
        # what if we don't know that function yet? 
        return env.get(name).compile_call(env, *args)

@case
class Number(value):
    def compile(self, env):
        if self.value < 0:
            return "0" + Number(-self.value).compile(env) + "-"
        nines, leftover = divmod(self.value, 9)
        if not nines: 
            return str(leftover)
        result = "9" * nines + '+' * (nines-1)
        if leftover: 
            result += str(leftover) + "+"
        return result

    def position_get_expr(self, env):
        return self.compile(env) + "<"

#############################

def allocate(env, expr = None):
    # We never clean up function calls? Do a set-based solution instead?
    position = Number(GlobalEnviroment.get('CurrentCell'))
    GlobalEnviroment.set('CurrentCell', position.value + 1)
    if expr is None:
        # pop from stack
        compiled_expr = ""
    else:
        compiled_expr = expr.compile(env)
    return position, compiled_expr + position.compile(env) + ">"

@case
class Function(start_position, param_names, body):
    assert len(body) > 0
    self.compiled_body = ""
    self.env = Enviroment.Local(GlobalEnviroment)

    def update_body(self):
        for param in reversed(self.param_names.value):
            position, compiled_expr = allocate(self.env)
            self.env.set(param, position)
            self.compiled_body += compiled_expr
        self.compiled_body += "".join(e.compile(self.env) for e in self.body)

    def compile_call(self, args):
        # 1. push all args
        # 2. jump to start position
        # 3. profit
        assert(len(args) == len(self.param_names))
        s = ""
        for arg_expr in args:
            s += arg_expr.compile()
        s += self.start_position.compile(env) + "c"
        return s

############################

@case
class Enviroment():
    class Local(parent, _mapping | {}):
        def get(self, what):
            if str(what) in self._mapping:
                return self._mapping[str(what)]
            return self.parent.get(what)

        def set(self, what, value):
            print "Setting", what, "to", value
            self._mapping[str(what)] = value

        def get_env(self, what):
            if what in self._mapping: 
                return self
            return parent.get_env(what)

        def set_where_defined(self, what, value):
            self.get_env(what).set(what, value)

    class Nil: 
        def get(self, what):
            raise ValueError("Could not find "+str(what))
        self.get_env = self.get

GlobalEnviroment = Enviroment.Local(Enviroment.Nil())

#############################
def compile(program, startCell = 500):
    from parser import program_parser
    from functions import *
    global GlobalEnviroment
    GlobalEnviroment = Enviroment.Local(Enviroment.Nil())
    GlobalEnviroment.set('CurrentCell', startCell)
    parsed_program = program_parser.parse(program)
    result = ""
    for expr in parsed_program:
        GlobalEnviroment.set('CurrentPosition', len(result))
        result += expr.compile(GlobalEnviroment)
    return result