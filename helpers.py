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


MAX = (float("inf"), "-"*9990)
def fastest(n, depth = 0, cache = {}):
    if n in range(10): 
        return "" if n == 0 and depth else str(n)
    if n not in cache:
        s = lambda x: (len(x), x)
        cache[n] = s("9" + fastest(n-9, depth+1) + "+")
        for i in range(1, 10):
            cache[n] = min(cache[n], 
                            s(str(i) + fastest(n-i, depth+1) + "+"))
            try:
                if depth>2: cache[n] = min(cache[n], s(str(i) + fastest(n+i, depth+1) + "-"))
            except: pass
            if i > 1 and n % i == 0:
                cache[n] = min(cache[n], s(str(i) + fastest(n/i, depth+1) + "*"))
    return cache[n][1]

for i in range(20000): fastest(i)