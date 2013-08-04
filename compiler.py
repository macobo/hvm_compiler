from macropy.quick_lambda import macros, f
from macropy.case_classes import macros, case

from parser import *

from helpers import fastest

@case
class CompileEnviroment(mapping | None):
    if self.mapping is None:
        self.mapping = {}

    def get(self, element):
        if element not in self.mapping:
            raise ValueError("Could not find "+str(element))
        return self.mapping[element]

    def set(self, element, value):
        self.mapping[element] = value

    # The following gives this class more of a namedtuple-like behaviour
    # when needed:
    # > CompileEnviroment().position = 5
    def __getattr__(self, element):
        return self.get(element)

    def __setattr__(self, element, value):
        self.set(element, value)


def compile(env, ast_element):
    # TODO: do we want to do this?
    if isinstance(ast_element, str):
        return ast_element
    if isinstance(ast_element, int):
        c = fastest(ast_element)
        return "0" + c + "-" if ast_element < 0 else c
    return ast_element.compile(env)


def compile_program(program_text):
    from functions import register_functions

    env = CompileEnviroment()
    register_functions(env)

    result = ""
    for command in parse_program(program_text):
        env.compile_position = len(result)
        result += compile(env, command)
    return result