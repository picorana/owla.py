from pprint import pprint
from monet.classes import OWLClass
from monet.classes import Ontology
from monet.classes import properties
from monet.classes import NamedIndividual
from monet.classes import Restriction
from monet.classes import AnonymousAncestor
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
            else:
                for item in list(elem):
                    if etree.QName(item.tag).localname == "Restriction":
                        new_class.restrictions.add(parse_restriction(result, item, auto_add))

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

        elif tag_name_child == "equivalentClass":
            new_class.equivalentClass.add(parse_anonymous_class(result, child))
        elif tag_name_child == "unionOf":
            new_class.unionOf.add(parse_anonymous_class(result, child))
        elif tag_name_child == "intersectionOf":
            new_class.intersectionOf.add(parse_anonymous_class(result, child))

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


def parse_restriction(result, child, auto_add):
    new_res = Restriction.Restriction()

    for item in list(child):
        tag_name_item = etree.QName(item.tag).localname

        # fill up all the fields of the restriction
        if tag_name_item == "onProperty":
            # Should check if property exists first!!
            new_res.onProperty = \
                next((result.get_property(uri=item.attrib[item2]) for item2 in item.attrib
                      if etree.QName(item2).localname == "resource"), None)

        elif tag_name_item == "someValuesFrom":
            if len(item.attrib) > 0:
                tmp_uri = next(item.attrib[x] for x in item.attrib)
                if result.has_class(uri=tmp_uri):
                    new_res.someValuesFrom = result.get_class(uri=tmp_uri)
                elif auto_add:
                    result.add_class(OWLClass(uri=tmp_uri))
                    new_res.someValuesFrom = result.get_class(uri=tmp_uri)

        elif tag_name_item == "allValuesFrom":
            if len(item.attrib) > 0:
                tmp_uri = next(item.attrib[x] for x in item.attrib)
                if result.has_class(uri=tmp_uri):
                    new_res.allValuesFrom = result.get_class(uri=tmp_uri)
                elif auto_add:
                    result.add_class(OWLClass(uri=tmp_uri))
                    new_res.allValuesFrom = result.get_class(uri=tmp_uri)

        elif tag_name_item == "minCardinality":
            new_res.minCardinality = item.text

        elif tag_name_item == "maxCardinality":
            new_res.maxCardinality = item.text

    return new_res


def parse_anonymous_class(result, item):
    new_anon_class = AnonymousAncestor.AnonymousAncestor()
    return new_anon_class