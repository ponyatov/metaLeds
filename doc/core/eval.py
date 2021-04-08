class Object:
    ## Lisp eval() in context
    def eval(self, env):
        raise NotImplementedError(['eval', self, env])
