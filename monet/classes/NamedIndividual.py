class NamedIndividual(object):

    label = None
    uri = None

    def __init__(self, label = None, uri=None):
        self.label = label
        self.uri = uri