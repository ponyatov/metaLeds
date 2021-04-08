class Number(Primitive):

    # print with preselected number of digits (rounded)
    def val(self):
        if self.value == None: return Nil.html
        if isinstance(self.value, float):
            if not self.prec:
                return f'{int(self.value)}'
            else:
                return f'{round(self.value,self.prec)}'
        raise TypeError(['val', type(self.value), self.value])
