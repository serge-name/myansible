from jinja2.runtime import Undefined

class FilterModule(object):
    ''' A comment '''

    def filters(self):
        return {
            'second': self.second,
        }

    def second(self, input_value):
        try:
            i = iter(input_value)
            i.next()
            return i.next()
        except StopIteration:
            # FIXME: supposed to raise an exception but it doesn't happen
            return Undefined()
