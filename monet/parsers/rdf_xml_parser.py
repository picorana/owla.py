from pprint import pprint
from monet.classes import *


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
            result.URI = about

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

            new_individual = NamedIndividual(uri=about)

            for elem in list(child):
                tag_name_child = etree.QName(elem.tag).localname
                if tag_name_child in string_properties:
                    new_individual.__dict__[tag_name_child] = elem.text

            result.add_individual(new_individual)

    pprint(str(result))

    return result
