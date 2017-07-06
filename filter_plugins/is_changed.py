class FilterModule(object):
    ''' A comment '''

    def filters(self):
        return {
            'is_changed': self.is_changed,
        }

    def is_changed(self, input_value, key, value):
        if type(input_value) is not dict:
            raise TypeError, u"{} must be dict (got {})".format(input_value, str(type(input_value)))

        if input_value.has_key('results'):
            res = input_value['results']
        else:
            res = [input_value]

        for item in res:
            if item.has_key(key) and item.has_key('changed'):
                if item[key] == value and item['changed'] == True:
                    return True

        return False
