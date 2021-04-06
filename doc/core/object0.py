class Object:
    def __init__(self,V):
        # scalar value: name, string, number,..
        self.value = V
        # slot{}s = attributes = associative array = env = map
        self.slot  = {}
        # nest[]ed = ordered container = vector = stack = AST
        self.nest  = []
        # global identifier: to distinct and address objects
        self.gid   = id(self)
