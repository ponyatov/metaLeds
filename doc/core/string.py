class String(Primitive):
    # dump strings in a single line with \escaped controls
    def val(self):
        ret = ''
        for c in self.value:
            if    c == '\n': ret += '\\n'
            elif  c == '\t': ret += '\\t'
            else: ret += c
        return ret
