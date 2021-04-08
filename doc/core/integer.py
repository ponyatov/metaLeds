class Integer(Number):
    def __init__(self, V):
        Primitive.__init__(self, int(V))
        self.prec = 0

    def val(self):
        if self.value == None: return Nil.html
        if isinstance(self.value, int):
            return f'{self.value}'
        raise TypeError(['val', type(self.value), self.value])
