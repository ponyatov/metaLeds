import os, sys, re
import datetime as dt

## base object graph node class = Marvin Minsky's Frame
class Object:
    def __init__(self, V):
        ## scalar value: name, string, number,..
        self.value = V
        ## associative array = environment = hash map
        self.slot = {}
        ## ordered container = vector = stack = nested ASTs
        self.nest = []
        ## global identifier: to distinct and address objects
        self.gid = id(self)

    ## @name tree-like text dump

    ## `print` callback
    def __repr__(self): return self.dump()
    ## used in `pytest`s
    def test(self): return self.dump(test=True)

    ## full text dump
    def dump(self, cycle=[], depth=0, prefix='', test=False):
        # header
        ret = self.pad(depth) + self.head(prefix, test)
        # block recursion on cyclic references
        if not depth: cycle = []
        if self.gid in cycle: return ret + ' _/'
        else: cycle.append(self.gid)
        # slot{}s
        for i in sorted(self.keys()):
            ret += self[i].dump(cycle, depth + 1, f'{i} = ', test)
        # nest[]ed
        for j, k in enumerate(self.nest):
            ret += k.dump(cycle, depth + 1, f'{j}: ', test)
        # subgraph
        return ret

    ## tree padding proportinal to recursion depth
    def pad(self, depth): return '\n' + '\t' * depth

    ## short single line <T:V> header
    def head(self, prefix='', test=False):
        gid = '' if test else f' @{self.gid:x}'
        return f'{prefix}<{self.tag()}:{self.val()}>{gid}'

    ## type/class tag
    def tag(self): return self.__class__.__name__.lower()

    ## value represented for dumps (shorted strings,..)
    def val(self): return f'{self.value}'

    ## @name operator

    ## `A.keys()` sorted slot keys
    def keys(self):
        return sorted(self.slot.keys())

    ## `iter(A)` iterator: `for i in Object():`
    def __iter__(self): return iter(self.nest)

    ## `A[key]` get node slot/nest element by name or index
    def __getitem__(self, key):
        if isinstance(key, str): return self.slot[key]
        if isinstance(key, int): return self.nest[key]
        raise TypeError(['__getitem__', type(key), key])

    ## `A[key] = B` assign by name/index
    def __setitem__(self, key, that):
        assert isinstance(that, Object)
        if isinstance(key, str): self.slot[key] = that; return self
        if isinstance(key, int): self.nest[key] = that; return self
        raise TypeError(['__setitem__', type(key), key])

    ## `A << B -> A[B.tag] = B` left/tag slot assignment
    def __lshift__(self, that):
        assert isinstance(that, Object)
        return self.__setitem__(that.tag(), that)

    ## `A >> B -> A[B.val] = B` right/val slot assignment
    def __rshift__(self, that):
        assert isinstance(that, Object)
        return self.__setitem__(that.val(), that)

    ## `A // B -> A.push(V)` stack-like push to end of vector
    def __floordiv__(self, that):
        assert isinstance(that, Object)
        self.nest.append(that); return self


hello = Object('hello'); hello // hello; print(hello)
world = Object('world'); hello // world; print(hello)
hello << Object('left') >> Object('right'); print(hello)
for i in hello: print('iter', i.head())
