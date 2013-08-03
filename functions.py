from eval import *
from macropy.case_classes import macros, case

def globalFunction(name):
    """ Wrap a globally defined function. 
        Each such function should return a compiled string """
    def wrap(f):
        wrap.compile_call = f
        GlobalEnviroment.set(Symbol(name), wrap)
        return f
    return wrap

def compile(expr, *args):
    if isinstance(expr, str):
        return expr
    return expr.compile(*args)

def compile_args(dont_compile):
    """
    Decorator that does the tedious job of compiling arguments for you.
    The first argument (Enviroment) is automatically skipped.

    This means can replace this:
        def add(env, a, b):
            compiled_a = compile(a, env)
            compiled_b = compile(b, env)
            return compiled_a + compiled_b + "+"

    With:
        @compile_args
        def add(env, a, b):
            return a + b + "+"

    You can also define it to skip other arguments:

        @compile_args(dont_compile=[3])
        def f(env, compiled_a, compiled_b, not_compiled): ...
    """
    def compile_args(args):
        env = args[0]
        return [a if i in dont_compile else compile(a, env) for i, a in enumerate(args)]

    def call(f):
        def _inner_call(*args):
            return f(*compile_args(args))
        return _inner_call

    if isinstance(dont_compile, list):
        dont_compile = set(dont_compile + [0]) # do not compile env
        return call
    # got a function directly
    f, dont_compile = dont_compile, set([0])
    return call(f)


@globalFunction('defun')
def DefineFunction(env, name, parameters, *body):
    global_position = GlobalEnviroment.get("CurrentPosition")
    # memory_position - position, where the start of the function
    # is saved
    memory_position, save_to_mem = allocate(GlobalEnviroment)
    function = Function(memory_position, parameters, body)

    GlobalEnviroment.set(name, function)
    c_body = function.compiled_body()
    c_skip = skip_block(c_body)

    start_position = global_position + len(c_skip)
    s = c_skip + c_body 
    # after a function declaration, save the start position to mem
    s+= Number(start_position).compile() + save_to_mem
    return s


@globalFunction('define')
def DefineVariable(env, name, expr):
    try:
        # TODO: is this right semantics for global/nonglobal? Think not
        position = env.get(name)
        compiled_expr = compile(expr, env) + compile(position, env) + ">"
    except:
        # name was not defined => allocate memory
        position, compiled_expr = allocate(env, expr)
        env.set(name, position)
    return compiled_expr


@globalFunction('if')
@compile_args(dont_compile=[3])
def IfElse(env, condition, true_branch, false_branch = None):
    # condition - 0 is false, anything else is True
    # CONDITIONAL_JUMP TRUE_BRANCH SKIP_TO_END FALSE_BRANCH
    c_true = compile(true_branch, env)
    cond = compile(condition, env)
    if false_branch is None:
        return cond + skip_block(c_true, conditional=True) + c_true

    c_false = compile(false_branch, env)
    skip_to_end = skip_block(c_false)

    s = cond
    s+= skip_block(c_true + skip_to_end, conditional=True)
    s+= c_true + skip_to_end + c_false
    return s

@globalFunction("do_while")
@compile_args
def do_while(env, condition, *body):
    # body, condition, conditional jump to start
    # This needs balancing, since the length of the jump
    # depends on the length of the jump block.
    # lower bound on length is body+condition+4 (09-g)
    # start trying from lower bound until len(body+cond+jump_block) <= lower_bound,
    # pad the jump block with spaces if neccessary
    body = "".join(body)
    condition = not_(env, condition)
    body_len = len(body) + len(condition)
    jump_block = lambda x: compile(Number(-x)) + "?"
    #print "%s (%d), %s (%d)" % (body, len(body), condition, len(condition))
    from itertools import count
    for jump_length in count(body_len + 4):
        spaces_needed = jump_length - (body_len + len(jump_block(jump_length)))
        #print "Jump length %d, jumper: %s, need %d extra spaces" % (jump_length, jump_block(jump_length), spaces_needed)
        if spaces_needed >= 0:
            return body + condition + " " * spaces_needed + jump_block(jump_length)


@globalFunction('print_num')
@compile_args
def printNumber(env, number):
    return number + "p"

@globalFunction('print_string')
def printString(env, data):
    return "".join(compile(Number(ord(x)), env)+"P" for x in data)

@globalFunction('print')
def printer(env, *args):
    def mapper(arg):
        if isinstance(arg, str): 
            return printString(env, arg)
        return printNumber(env, arg)
    return "".join(mapper(a) for a in args)


@globalFunction('mem')
@compile_args
def getMemoryAtPosition(env, memory_pos):
    return memory_pos + "<"



@globalFunction('setmem')
@compile_args
def getMemoryAtPosition(env, memory_pos, value):
    return value + memory_pos + ">"

@globalFunction('SetMemoryStart')
def setMemoryStart(env, position):
    GlobalEnviroment.set('CurrentCell', position.value)
    return ""

@globalFunction('begin')
def block(env, *body):
    childenv = Enviroment.Local(env)
    return "".join(compile(e, childenv) for e in body)


#### Arithmetic

pasteTogether = lambda env, *args: "".join(compile(arg, env) for arg in args)

globalFunction("+")(lambda *a: pasteTogether(*a) + "+" * (len(a)-2))
globalFunction("-")(lambda *a: pasteTogether(*a) + "-" * (len(a)-2))
globalFunction("*")(lambda *a: pasteTogether(*a) + "*" * (len(a)-2))
globalFunction("/")(lambda *a: pasteTogether(*a) + "/" * (len(a)-2))

@globalFunction("not")
def not_(env, a):
    return IfElse(env, a, Number(0), Number(1))


@globalFunction("!=")
@compile_args
def not_equals(env, a, b):
    return a + b + ":"

globalFunction(">=")(lambda *a: not_equals(*a) + "1+")
globalFunction("<=")(lambda *a: not_equals(*a) + "1-")
 
globalFunction("=")(lambda e, a, b: not_(e, not_equals(e, a, b)))

@globalFunction("and")
def and_(env, *a):
    if len(a) == 2: 
        x, y = a
        return IfElse(env, x, y, Number(0))
    return IfElse(env, a[0], and_(env, *a[1:]), Number(0))