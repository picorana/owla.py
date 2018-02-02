class OWLProperty(object):
    """
    Describes a property.
    """
    comment = None
    about = None
    label = None

    def __init__(self, comment=None, about=None, label=None):
        self.comment = comment
        self.about = about
        self.label = label


class DataProperty(OWLProperty):
    """
    Describes a data property.
    """

    value = None
    mimetype = None

    def __init__(self, comment=None, about=None, label=None, mimetype=None, value=None):
        super().__init__(comment, about, label)
        self.mimetype = mimetype
        self.value = value

    def __str__(self):
        return str(self.name) + " " + str(self.value)


class ObjectProperty(OWLProperty):
    """
    Describes an object property.
    """

    def __init__(self, comment=None, about=None, label=None):
        super().__init__(comment, about, label)
