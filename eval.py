from macropy.case_classes import macros, case

from helpers import fastest
import pprint

@case
class Symbol(value): 
    def compile(self, env):
        position = env.get(self)
        value = position.get_value_from_memory(env)
        print "\t", self, " - Getting from memory pos",position,":", value
        return value

@case
class List(value): 
    @staticmethod
    def c(first, rest):
        return List([first] + rest if first else [])

    def compile(self, env):
        if not self.value: return ""
        name, args = self.value[0], self.value[1:]
        print "Calling",name.value,"with",args
        # what if we don't know that function yet? 
        return env.get(name).compile_call(env, *args)

    def __len__(self): return len(self.value)

@case
class Number(value):
    def compile(self, env = None):
        if self.value < 0:
            return "0" + Number(-self.value).compile(env) + "-"

        return fastest(self.value)


#############################

@case
class Memory:
    class Position(value):
        def compile(self, env = None):
            return Number(self.value).compile(env)

        def get_value_from_memory(self, env = None):
            return self.compile(env) + "<"

    #class Range(start, end):

def allocate(env, expr = None):
    # We never clean up function calls? Do a set-based solution instead?
    position = Memory.Position(GlobalEnviroment.get('CurrentCell'))
    GlobalEnviroment.set('CurrentCell', position.value + 1)
    if expr is None:
        # pop from stack
        compiled_expr = ""
    else:
        compiled_expr = expr.compile(env)
    return position, compiled_expr + position.compile(env) + ">"


def skip_block(compiled_block, conditional = False):
    jumpSign = "?" if conditional else "g"
    return Number(len(compiled_block)).compile() + jumpSign


@case
class Function(start_position, param_names, body):
    assert len(body) > 0
    self._compiled_body = ""
    self.env = Enviroment.Local(GlobalEnviroment)

    def compiled_body(self):
        if self._compiled_body != "":
            return self._compiled_body
        for param in reversed(self.param_names.value):
            position, compiled_expr = allocate(self.env)
            self.env.set(param, position)
            self._compiled_body += compiled_expr
        print "\tparams-part", self._compiled_body
        self._compiled_body += "".join(e.compile(self.env) for e in self.body)
        self._compiled_body += "$"
        print "\tcompiled to", self._compiled_body

        return self._compiled_body

    def body_start_position(self):
        return self.start_position.get_value_from_memory()

    def compile_call(self, old_env, *args):
        # 1. push all args to stack
        # 2. jump to start position
        # 3. profit
        assert(len(args) == len(self.param_names))
        s = ""
        for arg_expr in args:
            s += arg_expr.compile(old_env)
        s += self.body_start_position() + "c"
        return s

############################

@case
class Enviroment():
    class Local(parent):
        self._mapping = {}
        def get(self, what):
            if str(what) in self._mapping:
                return self._mapping[str(what)]
            return self.parent.get(what)

        def set(self, what, value):
            self._mapping[str(what)] = value
            print "Setting", what, "to", value, self==GlobalEnviroment

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

        def __str__(self): return "-"

GlobalEnviroment = Enviroment.Local(Enviroment.Nil())

#############################
def compiler(program, startCell = 500):
    from parser import program_parser
    from functions import *
    global GlobalEnviroment
    #GlobalEnviroment = Enviroment.Local(Enviroment.Nil())
    GlobalEnviroment.set('CurrentCell', startCell)
    parsed_program = program_parser.parse(program)
    result = ""
    for expr in parsed_program:
        GlobalEnviroment.set('CurrentPosition', len(result))
        #pprint.pprint(GlobalEnviroment._mapping)
        result += expr.compile(GlobalEnviroment) 
        result += " "*8
    return result