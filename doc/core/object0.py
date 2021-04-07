class Object:
    def __init__(self,V):
        ## scalar value: name, string, number,..
        self.value = V
        ## associative array = environment = hash map
        self.slot  = {}
        ## ordered container = vector = stack = nested ASTs
        self.nest  = []
        ## global identifier: to distinct and address objects
        self.gid   = id(self)
