class Object:

    ## `A[key] = B` assign by name/index
    def __setitem__(self, key, that):
        that = self.box(that)
        if isinstance(key, str): # slot[str]
            self.slot[key] = that; return self
        if isinstance(key, int): # nest[int]
            self.nest[key] = that; return self
        raise TypeError(['__setitem__', type(key), key])
