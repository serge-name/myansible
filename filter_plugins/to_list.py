class FilterModule(object):
    ''' A Comment '''

    def filters(self):
        return {
            'to_list': self.to_list,
        }

    def to_list(self,input_value):
        import ansible

        if type(input_value) is list:
            return input_value
        elif type(input_value) in [str, unicode, ansible.parsing.yaml.objects.AnsibleUnicode]:
            return [input_value]
        else:
            raise TypeError, u"{} must be either list or str (got {})".format(input_value, str(type(input_value)))
