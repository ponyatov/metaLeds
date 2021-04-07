 
## `A.keys()` sorted slot keys
def keys(self): return self.slot.keys()

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
