from eval import *
from macropy.case_classes import macros, case

def globalFunction(name):
    """ Wrap a globally defined function. 
        Each such function should return compiled_fun: string """
    def wrap(f):
        wrap.compile_call = f
        GlobalEnviroment.set(Symbol(name), wrap)
        return f
    return wrap

def compile(expr, *args):
    if isinstance(expr, str):
        return expr
    return expr.compile(*args)


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



@globalFunction('print_num')
def printNumber(env, number):
    return compile(number, env) + "p"


@globalFunction('mem')
def getMemoryAtPosition(env, pos_expr):
    memory_pos = compile(pos_expr, env)
    return memory_pos + "<"


@globalFunction('setmem')
def getMemoryAtPosition(env, pos_expr, value):
    return compile(value, env) + compile(pos_expr, env) + ">"


@globalFunction('block')
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
def not_equals(env, a, b):
    return pasteTogether(env, a, b) + ":"

globalFunction("<=")(lambda *a: not_equals(*a) + "1+")
globalFunction(">=")(lambda *a: not_equals(*a) + "1-")
 
globalFunction("=")(lambda e, a, b: not_(e, not_equals(e, a, b)))