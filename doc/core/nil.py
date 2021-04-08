class Nil(Primitive):
    def __init__(self): super().__init__('')
    html = '\u2014'
    def html(self): return Nil.html
