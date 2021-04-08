## floating point
class Number(Primitive):
    def __init__(self, V, prec=4):
        Primitive.__init__(self, float(V))
        ## precision: digits after decimal `.`
        self.prec = prec
