from monet.classes import OWLClass
from monet.classes import properties
from monet.writers import *
from monet.constants import *
from lxml import etree


class Ontology(object):
    """
    An ontology.
    """

    URI = None
    classes = set()
    properties = set()
    individuals = set()

    def __init__(self, URI = None):
        self.URI = URI
        self.classes = set()
        self.properties = set()
        self.individuals = set()

    def __str__(self):
        return "classes: " + str([c.__dict__ for c in self.classes]) + " \n " \
               + "properties: " + str([p.__dict__ for p in self.properties]) + "\n" \
               + "individuals" + str([i.__dict__ for i in self.individuals])

    def add_class(self, new_class):
        if self.has_class(uri=new_class.uri):
            raise RuntimeError("class label " + new_class.label + " already assigned")
        else:
            self.classes.add(new_class)

    def has_class(self, uri=None, label=None):
        """
        Returns True if the ontology contains the specified class, False otherwise.
        You can search classes by label or uri, please specify at least one of them when calling the function.

        :param uri: uri of the class
        :param label: label of the class
        :return: boolean
        """
        if uri is not None and True in (c.uri == uri for c in self.classes):
            return True
        elif label is not None and True in (c.label == label for c in self.classes):
            return True
        else:
            return False

    def get_class(self, uri=None, label=None):
        """
        Returns an OWLClass in the ontology. Please, specify at least one among uri and label.

        :param uri: URI address of the class
        :param label: label of the class
        :return: OWLClass corresponding to the label or uri.
        """
        if uri is not None and self.has_class(uri=uri):
            return next(c for c in self.classes if c.uri == uri)
        elif label is not None and self.has_class(label=label):
            return next(c for c in self.classes if c.label == label)
        else:
            raise RuntimeError("class not found in this ontology")

    def remove_class(self, target_class):
        # need to remove the class from all relationships, and remove all the properties that use this class
        self.classes.discard(target_class)

    def has_property(self, uri=None, label=None):
        """

        :param uri:
        :param label:
        :return:
        """
        if uri is not None and True in (c.uri == uri for c in self.properties):
            return True
        elif label is not None and True in (c.label == label for c in self.properties):
            return True
        else:
            return False

    def add_property(self, new_property):
        self.properties.add(new_property)

    def remove_property(self, target_property):
        # may need to remove the property from all the classes that have it
        self.properties.discard(target_property)

    def get_property(self, uri=None, label=None):
        """

        :param uri:
        :param label:
        :return:
        """
        if uri is not None and self.has_property(uri=uri):
            return next(c for c in self.properties if c.uri == uri)
        elif label is not None and self.has_property(label=label):
            return next(c for c in self.properties if c.uri == label)
        else:
            raise RuntimeError("class not found in this ontology")

    def add_individual(self, new_individual):
        self.individuals.add(new_individual)

    def has_individual(self, target_individual):
        return True in (c.label == target_individual for c in self.individuals)

    def remove_individual(self, target_individual):
        self.individuals.discard(target_individual)

    def get_individual(self, label):
        if self.has_individual(label):
            return next(c.label == label for c in self.individuals)
        else:
            raise RuntimeError("class " + label + "not found in this ontology")

    def save(self, output_path=OUTPUT_PATH, syntax="rdf/xml"):
        write_ontology(self, output_path, syntax)







