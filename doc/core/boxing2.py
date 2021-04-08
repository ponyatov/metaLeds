class Object:

    ## `A << B -> A[B.tag] = B` left/tag slot assignment
    def __lshift__(self, that):
        that = self.box(that)
        return self.__setitem__(that.tag(), that)

    ## `A // B -> A.push(B)` stack-like push to end of vector
    def __floordiv__(self, that):
        that = self.box(that)
        self.nest.append(that); return self
