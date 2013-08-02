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
    position = GlobalEnviroment.get("CurrentPosition")
    function = Function(position, parameters, body)
    GlobalEnviroment.set(name, function)
    return function.skip_body() + function.compiled_body()


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
def If(env, condition, body): 
    compiled_condition = condition.compile(env)
    compiled_body = body.compile(env)
    s = compiled_condition # result goes to S0
    # jump over body if S0
    s += Number(len(compiled_body)).compile(env) + '?'
    s += compiled_body
    return s


@globalFunction('ifelse')
def IfElse(env, condition, true_branch, false_branch): pass


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