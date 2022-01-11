import os


class FilterModule(object):
    """
    Returns file's basename and strips a suffix if defined:

        {{ some_path |basename }}
        {{ another_path |basename('.tar.gz') }}
    """

    def filters(self):
        return {
            'basename': self.basename,
        }

    def basename(self, input_value, suffix=None):
        if suffix and input_value.endswith(suffix):
            return os.path.basename(input_value[:-len(suffix)])
        else:
            return os.path.basename(input_value)
