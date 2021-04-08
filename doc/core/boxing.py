class Object:

    ## Python types boxing
    def box(self, that):
        # metaL types: returns as is
        if isinstance(that, Object): return that
        # Python
        if isinstance(that, int): return Integer(that)
        if isinstance(that, str): return String(that)
        if that == None: return Nil()
        # unknown
        raise TypeError(['box', type(that), that])
