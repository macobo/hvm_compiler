from macropy.quick_lambda import macros, f

def memoize(f):
    f.cache = {}
    def call(*args):
        if args not in cache:
            f.cache[args] = f(*args)
        return f.cache[args]
    return call

def evaluate_number(x):
    o_dict = {
        "+": f[_+_],
        "-": f[_-_],
        "*": f[_*_],
        "/": f[_/_],
    }
    result, stack = 0, []
    for token in x:
        if token in o_dict: 
            a, b = stack.pop(), stack.pop()
            stack.append(o_dict[token](b, a))
        else:               
            stack.append(int(token))
    return tuple(stack)