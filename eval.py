from macropy.case_classes import macros, case

@case
class Symbol(value): 
    def compile(self, env):
        raise ValueError(self + " cannot be compiled")

@case
class List(value): 
    @staticmethod
    def c(first, rest):
        return List([first] + rest if first else [])

@case
class Number(value):
    def compile(self, env):
        if self.value < 0:
            return "0" + Number(-self.value).compile(env) + "-"
        nines, leftover = divmod(self.value, 9)
        if not nines: 
            return str(leftover)
        result = "9" * nines + '+' * (nines-1)
        if leftover: 
            result += str(leftover) + "+"
        return result

@case
class Enviroment():
    class Local(parent):
        _mapping = {}

        def find(self, what):
            if what in self._mapping:
                return self._mapping[what]
            return self.parent.find(what)

        def set(self, what, value):
            self._mapping[what] = value

    class Nil(): 
        def find(self, what):
            raise ValueError("Could not find "+what)