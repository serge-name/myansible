class FilterModule(object):
    ''' If input is string, just return the string; if array, merge elements '''

    def filters(self):
        return {
            'smart_join': self.smart_join,
        }

    def smart_join(self,input_value):
        if type(input_value) is str:
            return input_value
        elif type(input_value) is list:
            return "\n".join(input_value)
        else:
            raise
