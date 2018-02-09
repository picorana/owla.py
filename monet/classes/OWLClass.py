class OWLClass(object):
    """
    Describes a class in a ontology.
    """

    uri = None
    properties = set()
    comment = None
    subClassOf = set()
    equivalentClass = set()
    unionOf = set()
    intersectionOf = set()
    disjointWith = set()
    restrictions = set()
    label = None

    def __init__(self, uri=None, comment=None, label=None):

        # todo:
        # can classes have no name?

        self.uri = uri
        self.comment = comment
        self.label = label
        self.subClassOf = set()
        self.disjointWith = set()
        self.restrictions = set()
        self.unionOf = set()
        self.intersectionOf = set()
        self.equivalentClass = set()

    def add_property(self, new_property):
        self.properties.add(new_property)

    def remove_property(self, target_property):
        self.properties.discard(target_property)

    def __repr__(self):
        to_str = ""
        if self.uri is not None:
            to_str += "uri: " + self.uri + "\n"
        if self.label is not None:
            to_str += "label: " + self.label + "\n"
        if self.comment is not None:
            to_str += "comment: " + self.comment + "\n"
        if self.restrictions is not None and len(self.restrictions) > 0:
            to_str += "restrictions: \n"
            for elem in self.restrictions:
                to_str.join(e for e in elem.__dict__) + "\n"
        if self.subClassOf is not None and len(self.subClassOf) > 0:
            to_str += "subClassOf: \n "
            for elem in self.subClassOf:
                to_str += str(elem) + " \n "
        if self.disjointWith is not None and len(self.disjointWith) > 0:
            to_str += "disjointWith: \n "
            for elem in self.disjointWith:
                to_str += str(elem) + " \n "
        return to_str