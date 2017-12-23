from jinja2.runtime import Undefined, StrictUndefined

class FilterModule(object):
    ''' A comment '''

    def filters(self):
        return {
            'is_empty': self.is_empty,
            'is_empty_or_undefined': self.is_empty_or_undefined,
        }

    def is_empty(self, input_value):
        return (input_value is None or len(input_value) == 0)

    def is_empty_or_undefined(self, input_value):
        return (type(input_value) in (StrictUndefined, Undefined, ) or
                self.is_empty(input_value))
