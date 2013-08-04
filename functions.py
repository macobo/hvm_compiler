from macropy.case_classes import macros, case
from compiler import compile
from parser import Symbol

all_functions = []

def function(name):
    def wrap(f):
        f.name = name
        all_functions.append((name, f))
        return f
    return wrap


def register_functions(enviroment):
    for name, func in all_functions:
        env.set(Symbol(name), function)


@case
class Constant(value):
    " Dummy class to store values "
    def compile(self, env):
        return compile(env, value)


@function("const")
def define_constant(env, name, value):
    env.set(name, Constant(value))
    return ""


@function("push")
def push(env, *args):
    """ Pushes all args to the top of the stack. 
        Note that if some argument is a string, it is treated as already compiled. """
    return "".join(map(compile, args))


@function("print_numbers")
def print_numbers(env, n=1):
    " Prints n first numbers from top of the stack "
    return "p" * n


@function("print_chars")
def print_chars(env, n=1):
    " Prints n first characters from top of the stack "
    return "P" * n


def backwards_jump(body_length, conditional):
    from itertools import count
    if body_length == 0: 
        return ""

    jump_char = "?" if conditional else "g"
    block_gen = lambda jump_len: compile(env, -jump_len) + jump_char
    for jump_length in count(body_length + 4):
        jump_block = block_generator(jump_length)
        padding_needed = jump_length - (body_length + len(jump_block))
        if padding_needed >= 0:
            return " " * padding_needed + jump_block


@function("jump")
def unconditional_jump(env, label = None):
    " Jumps to label. If no argument given, jump size is Stack[0] "
    if label is None: return "g"
    label_position = env.get(label)
    current_position = env.compile_position
    # TODO: we currently have no means of supporting forwards jumps
    return backwards_jump(current_position - label_position, False)


@function("conditional_jump")
def conditional_jump(env, label = None):
    " Jumps to label if stack[0] is 0. If no argument given, jump size is Stack[1] "
    if label is None: return "?"
    label_position = env.get(label)
    current_position = env.compile_position
    # TODO: we currently have no means of supporting forwards jumps
    return backwards_jump(current_position - label_position, True)



