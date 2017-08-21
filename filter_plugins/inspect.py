class FilterModule(object):
    ''' A comment '''

    def filters(self):
        return {
            'inspect': self.inspect,
        }

    def inspect(self, input_value, verbose=None):
        if (type(input_value) is list) and verbose:
            return "[{}]".format(",".join([str(type(i)) for i in input_value]))
        else:
            return str(type(input_value))
