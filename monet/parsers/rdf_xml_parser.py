from pprint import pprint
from monet.classes import OWLClass
from monet.classes import Ontology
from monet.classes import properties
from monet.classes import NamedIndividual
from monet.constants import *
from lxml import etree


def load_rdf_xml(filepath, auto_add = True):
    result = Ontology()

    parser = etree.XMLParser(remove_comments=True)
    tree = etree.parse(filepath, parser=parser)

    for child in list(tree.getroot()):

        about = next((child.attrib[key] for key in child.keys() if etree.QName(key).localname == "about"), None)
        tag_name = etree.QName(child.tag).localname

        if tag_name == "Ontology":
            result.URI = about

        elif tag_name == "ObjectProperty":
            parse_object_property(result, child, about)

        elif tag_name == "DatatypeProperty":
            parse_data_property(result, child, about)

        elif tag_name == "Class":
            # check equivalentClass and subClass
            parse_class(result, child, about, auto_add)

        elif tag_name == "NamedIndividual" or tag_name == "Thing":
            parse_named_individual(result, child, about, auto_add)

    #pprint(str(result))

    return result


def parse_object_property(result, child, about):
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


def parse_data_property(result, child, about):
    if result.has_property(uri=about):
        new_data_property = result.get_property(uri=about)
    else:
        new_data_property = properties.DataProperty(uri=about)

    result.add_property(new_data_property)


def parse_class(result, child, about, auto_add):
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

            # subClassOf
            if tag_name_child == "subClassOf":
                if len(elem.attrib) > 0:
                    for item in elem.attrib:
                        if result.has_class(uri=elem.attrib[item]):
                            new_class.subClassOf.add(result.get_class(uri=elem.attrib[item]))
                        elif auto_add:
                            new_subclass_class = OWLClass(uri=elem.attrib[item])
                            result.add_class(new_subclass_class)
                            new_class.subClassOf.add(new_subclass_class)
                        else:
                            raise RuntimeError(
                                "class " + elem.attrib[item] + " referenced in subClassOf axiom but not"
                                                               "found in the ontology, use auto_add"
                                                               "option to automatically add referenced"
                                                               "subclasses to the ontology")

            # disjointWith
            elif tag_name_child == "disjointWith":
                if len(elem.attrib) > 0:
                    for item in elem.attrib:
                        if result.has_class(uri=elem.attrib[item]):
                            new_class.disjointWith.add(result.get_class(uri=elem.attrib[item]))
                        elif auto_add:
                            new_disjoint_class = OWLClass(uri=elem.attrib[item])
                            result.add_class(new_disjoint_class)
                            new_class.disjointWith.add(new_disjoint_class)
                        else:
                            raise RuntimeError(
                                "class " + elem.attrib[item] + " referenced in subClassOf axiom but not"
                                                               "found in the ontology, use auto_add"
                                                               "option to automatically add referenced"
                                                               "subclasses to the ontology")

    if result.has_class(uri=new_class.uri):
        prev_class = result.get_class(uri=new_class.uri)
        prev_class = new_class
    else:
        result.add_class(new_class)


def parse_named_individual(result, child, about, auto_add):
    new_individual = NamedIndividual(uri=about)

    for elem in list(child):
        tag_name_child = etree.QName(elem.tag).localname
        if tag_name_child in string_properties:
            new_individual.__dict__[tag_name_child] = elem.text

    result.add_individual(new_individual)