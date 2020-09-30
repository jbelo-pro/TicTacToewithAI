def tagged(func):
    def wrapped(arg1):
        return r'<title>{}</title>'.format(func(arg1))
    return wrapped


@tagged
def from_input(inp):
    string = inp.strip()
    return string
