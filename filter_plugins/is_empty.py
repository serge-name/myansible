class FilterModule(object):
    ''' A comment '''

    def filters(self):
        return {
            'is_empty': self.is_empty,
        }

    def is_empty(self, input_value):
        if input_value is None or len(input_value) == 0:
            return True
        else:
            return False
