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
    for i in self.keys():
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
