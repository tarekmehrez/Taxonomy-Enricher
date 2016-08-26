"""Contains the config option class."""


class Option(object):

    """
    Create an option, assign a type and set its value.
    """

    def __init__(self, section, param, type, required, default_value):
        """
        Initialize option instance.

        params:
            param (str): param of item
            type (tuple(type)|type): type of item
            required (boolean): whether the item is required
            default_value
        """
        self.section = section
        self.param = param
        self.type = type
        self.required = required
        self.default_value = default_value
        self.value = default_value

    def set_value(self, value):
        """
        Set value of the config item.
        """
        if self.type == float:
            self.value = float(value)

        elif self.type == int:
            self.value = int(value)

        # type is list of a certain type, example (list, float)
        # saying the type is list of floats
        elif isinstance(self.type, tuple):
            list_type = self.type[1]
            parsed_values = value.split('\n')
            self.value = [list_type(item) for item in parsed_values]

        else:
            self.value = value
