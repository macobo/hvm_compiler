from eval import *

def globalFunctionWrapper(name):
    """ Wrap a globally defined function. 
        Each such function should return compiled_fun: string """
    def wrap(f):
        wrap.compile_call = f
        GlobalEnviroment.set(Symbol(name), wrap)
        return f
    return wrap

@globalFunctionWrapper('defun')
def DefineFunction(env, name, parameters, *body):
    position = GlobalEnviroment.get("CurrentPosition")
    function = Function(position, parameters, body)
    GlobalEnviroment.set(name, function)
    function.update_body()
    return function.compiled_body


@globalFunctionWrapper('define')
def DefineVariable(env, name, expr):
    try:
        position = env.get(name)
        compiled_expr = expr.compile(env) + position.compile(env) + ">"
    except:
        # name was not defined
        position, compiled_expr = allocate(env, expr)
        env.set(name, position)
    return compiled_expr


@globalFunctionWrapper('if')
def If(env, condition, body): 
    compiled_condition = condition.compile(env)
    compiled_body = body.compile(env)
    s = compiled_condition # result goes to S0
    # jump over body if S0
    s += Number(len(compiled_body)).compile(env) + '?'
    s += compiled_body
    return s


@globalFunctionWrapper('ifelse')
def IfElse(env, condition, true_branch, false_branch): pass


@globalFunctionWrapper('print_num')
def printNumber(env, number):
    return number.compile(env) + "p"