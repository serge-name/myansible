from jinja2.runtime import Undefined, StrictUndefined

class FilterModule(object):
    ''' A comment '''

    def filters(self):
        return {
            'attr_or_default': self.attr_or_default,
        }

    def attr_or_default(self, input_value, name, default):
        if type(input_value) not in (StrictUndefined, Undefined, ):
            # can't use getattr() since keys have type ansible.parsing.yaml.objects.AnsibleUnicode
            keys = filter((lambda k: k == name), input_value.keys())
            if len(keys) > 0:
                return input_value[keys[0]]

        return default
