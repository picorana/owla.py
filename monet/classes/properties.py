class Property(object):
    """
    Describes a property.
    """
    name = None

    def __init__(self, name=None):
        self.name = name


class DataProperty(Property):
    """
    Describes a data property.
    """

    value = None
    mimetype = None

    def __init__(self, name=None, mimetype=None, value=None):
        super().__init__(name)
        self.mimetype = mimetype
        self.value = value

    def __str__(self):
        return str(self.name) + " " + str(self.value)


class ObjectProperty(Property):
    """
    Describes an object property.
    """

    def __init__(self, name=None):
        super().__init__(name)
