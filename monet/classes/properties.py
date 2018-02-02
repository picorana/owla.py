class OWLProperty(object):
    """
    Describes a property.
    """
    comment = None
    uri = None
    label = None

    def __init__(self, comment=None, uri=None, label=None):
        self.comment = comment
        self.uri = uri
        self.label = label


class DataProperty(OWLProperty):
    """
    Describes a data property.
    """

    value = None
    mimetype = None

    def __init__(self, comment=None, uri=None, label=None, mimetype=None, value=None):
        super().__init__(comment, uri, label)
        self.mimetype = mimetype
        self.value = value


class ObjectProperty(OWLProperty):
    """
    Describes an object property.
    """

    def __init__(self, comment=None, uri=None, label=None):
        super().__init__(comment, uri, label)
