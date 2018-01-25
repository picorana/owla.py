from monet.classes import *

class Ontology(object):
    """
    An ontology.
    """

    URI = None
    classes = set()

    def __init__(self, URI = None):
        self.URI = URI
        self.classes.add(OntologyClass(name="owl:Thing"))

    def add_class(self, new_class):
        self.classes.add(new_class)


class OntologyClass(object):
    """
    Describes a class in a ontology.
    """

    name = None
    properties = set()
    is_a = None

    def __init__(self, name=None):

        # todo:
        # can classes have no name?
        # should they have a unique ID?

        self.name = name

    def add_property(self, property):
        self.properties.add(property)





