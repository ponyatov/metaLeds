class Object:
    ## Lisp apply() to `that` object in context
    def apply(self, env, that):
        raise NotImplementedError(['apply', self, env, that])
