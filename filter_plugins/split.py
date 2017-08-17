class FilterModule(object):
    ''' A comment '''

    def filters(self):
        return {
            'split': self.split,
        }

    def split(self, input_value, separator):
        return input_value.split(separator)
