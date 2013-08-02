from eval import *

def globalFunction(name):
    """ Wrap a globally defined function. 
        Each such function should return compiled_fun: string """
    def wrap(f):
        wrap.compile_call = f
        GlobalEnviroment.set(Symbol(name), wrap)
        return f
    return wrap


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
        compiled_expr = expr.compile(env) + position.compile(env) + ">"
    except:
        # name was not defined => allocate memory
        position, compiled_expr = allocate(env, expr)
        env.set(name, position)
    return compiled_expr


@globalFunction('if')
def IfElse(env, condition, true_branch, false_branch):
    # CONDITIONAL_JUMP TRUE_BRANCH SKIP_TO_END FALSE_BRANCH
    c_true = true_branch.compile(env)
    c_false = false_branch.compile(env)

    skip_to_end = skip_block(c_false)

    s = condition.compile(env)
    s+= skip_block(c_true + skip_to_end, conditional=True)
    s+= c_true + skip_to_end + c_false
    print (condition.compile(env), c_true, c_false)
    return s



@globalFunction('print_num')
def printNumber(env, number):
    return number.compile(env) + "p"


@globalFunction('mem')
def getMemoryAtPosition(env, position):
    memory_pos = Memory.Position(position.value)
    return memory_pos.get_value_from_memory(env)


#### Arithmetic

pasteTogether = lambda env, *args: "".join(arg.compile(env) for arg in args)

globalFunction("+")(lambda *a: pasteTogether(*a) + "+" * (len(a)-2))
globalFunction("-")(lambda *a: pasteTogether(*a) + "-" * (len(a)-2))
globalFunction("*")(lambda *a: pasteTogether(*a) + "*" * (len(a)-2))
globalFunction("/")(lambda *a: pasteTogether(*a) + "/" * (len(a)-2))


def not_equals(env, a, b):
    return pasteTogether(env, a, b) + ":"

globalFunction("<")(lambda *a: not_equals(*a) + "1-")
globalFunction(">")(lambda *a: not_equals(*a) + "1+")