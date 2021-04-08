## Variable name
class Name(Primitive):
    ## evaluates by name lookup in `env`
    def eval(self, env): return env[self.value]
