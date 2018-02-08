class OWLClass(object):
    """
    Describes a class in a ontology.
    """

    uri = None
    properties = set()
    comment = None
    subClassOf = set()
    equivalentClass = set()
    disjointWith = set()
    label = None

    def __init__(self, uri=None, comment=None, label=None):

        # todo:
        # can classes have no name?
        # should they have a unique ID?

        self.uri = uri
        self.comment = comment
        self.label = label
        self.subClassOf = set()
        self.disjointWith = set()

    def add_property(self, new_property):
        self.properties.add(new_property)

    def remove_property(self, target_property):
        self.properties.discard(target_property)