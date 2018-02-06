from monet.classes import properties
from lxml import etree
from pprint import pprint


def load_rdf_xml(filepath, auto_add = True):
    result = Ontology()

    parser = etree.XMLParser(remove_comments=True)
    tree = etree.parse(filepath, parser=parser)

    for child in list(tree.getroot()):

        about = next((child.attrib[key] for key in child.keys() if etree.QName(key).localname == "about"), None)
        tag_name = etree.QName(child.tag).localname

        properties_with_resources = {"subPropertyOf", "intersectionOf", "inverseOf", "disjointWith", "subClassOf", "equivalentClass", "domain", "range"}
        string_properties = {"comment", "label"}

        if tag_name == "Ontology":
            result.uri = about

        elif tag_name == "ObjectProperty":

            if result.has_property(uri=about):
                new_object_property = result.get_property(uri=about)
            else:
                new_object_property = properties.ObjectProperty(uri=about)

            for elem in list(child):
                tag_name_child = etree.QName(elem.tag).localname
                if tag_name_child in string_properties:
                    new_object_property.__dict__[tag_name_child] = elem.text
                elif tag_name_child in properties_with_resources:
                    new_object_property.__dict__[tag_name_child] = \
                        next((elem.attrib[key] for key in elem.keys() if etree.QName(key).localname == "resource"), None)

            result.add_property(new_object_property)

        elif tag_name == "DatatypeProperty":

            if result.has_property(uri=about):
                new_data_property = result.get_property(uri=about)
            else:
                new_data_property = properties.DataProperty(uri=about)

            result.add_property(new_data_property)

        elif tag_name == "Class":
            # check equivalentClass and subClass

            if result.has_class(uri=about):
                new_class = result.get_class(uri=about)
            elif auto_add:
                new_class = OWLClass(uri=about)
            else:
                raise RuntimeError("class " + about + " not found")

            for elem in list(child):
                tag_name_child = etree.QName(elem.tag).localname
                if tag_name_child in string_properties:
                    new_class.__dict__[tag_name_child] = elem.text
                if tag_name_child in properties_with_resources:
                    if tag_name_child == "subClassOf":
                        if len(elem.attrib)>0:
                            for item in elem.attrib:
                                if result.has_class(uri=elem.attrib[item]):
                                    new_class.subClassOf.add(result.get_class(uri=elem.attrib[item]))
                                #elif auto_add:
                                #    result.add_class(OWLClass(uri=elem.attrib[item]))

            result.add_class(new_class)

        # are named individuals and things exactly the same?
        elif tag_name == "NamedIndividual" or tag_name == "Thing":

            new_individual = NamedIndividual(about=about)

            for elem in list(child):
                tag_name_child = etree.QName(elem.tag).localname
                if tag_name_child in string_properties:
                    new_individual.__dict__[tag_name_child] = elem.text

            result.add_individual(new_individual)

    pprint(str(result))

    return result


def load_ontology_from_file(filepath, mode="rdf/xml"):
    """
    Returns an ontology from a file.

    :param filepath: specify the path of the file that contains the ontology to read
    :param mode: specify the syntax of the file. Possible modes are: "rdf/xml", "owl/xml". Default: rdf/xml.
    :return: Ontology
    """

    if mode=="rdf/xml":
        return load_rdf_xml(filepath)
    elif mode=="owl/xml":
        raise RuntimeError("mode not yet implemented")
    else:
        raise RuntimeError("mode not found")


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


class OWLClass(object):
    """
    Describes a class in a ontology.
    """

    uri = None
    properties = set()
    comment = None
    subClassOf = set()
    label = None

    def __init__(self, uri=None, comment=None, label=None):

        # todo:
        # can classes have no name?
        # should they have a unique ID?

        self.uri = uri
        self.comment = comment
        self.label = label
        self.subClassOf = set()

    def add_property(self, new_property):
        self.properties.add(new_property)

    def remove_property(self, target_property):
        self.properties.discard(target_property)


class NamedIndividual(object):

    label = None
    uri = None

    def __init__(self, label = None, uri=None):
        self.label = label
        self.uri = uri






