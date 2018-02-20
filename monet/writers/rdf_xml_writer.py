from monet.constants import *
from monet.classes import OWLClass


def rdf_xml_write(ontology, output_path):
    file_to_write = open(output_path, 'w')
    file_to_write.write(xml_head + "\n")

    rdf_xml_root = etree.Element(etree.QName(xmlns.rdf, 'RDF'), nsmap={
        "rdf": xmlns.rdf,
        "owl": xmlns.owl,
        "xml": xmlns.xml,
        "xsd": xmlns.xsd,
        "rdfs": xmlns.rdfs,
        "ns0": str(ontology.URI) + "#",
    })

    rdf_xml_root.attrib[etree.QName(xmlns.xml, "base")] = str(ontology.URI)
    rdf_xml_root.attrib["xmlns"] = str(ontology.URI) + "#"

    rdf_xml_root.append(etree.Element(etree.QName(xmlns.owl, "Ontology"),
                                      attrib={etree.QName(xmlns.rdf, "about"): str(ontology.URI)}))

    # go through all the components of the ontology, generate an XML element for each component
    for c in ontology.classes.union(ontology.properties).union(ontology.individuals):

        new_elem = etree.Element(etree.QName(xmlns.owl, rdf_xml_type_map[c.__class__.__name__]),
                                 attrib={etree.QName(xmlns.rdf, "about"): str(c.uri)})

        # comment
        comment_node = etree.Element(etree.QName(xmlns.rdfs, "comment"),
                                     attrib={etree.QName(xmlns.rdf, "datatype"): xmlns.xsd + "string"})
        if c.comment is not None: comment_node.text = c.comment
        new_elem.append(comment_node)

        # label
        label_node = etree.Element(etree.QName(xmlns.rdfs, "label"),
                                   attrib={etree.QName(xmlns.rdf, "datatype"): xmlns.xsd + "string"})
        if c.label is not None: label_node.text = c.label
        new_elem.append(label_node)

        # OWLClass specific
        if type(c) is OWLClass.OWLClass:

            # subClassOf
            if c.subClassOf is not None and len(c.subClassOf) > 0:
                for elem in c.subClassOf:
                    subclass_node = etree.Element(etree.QName(xmlns.rdfs, "subClassOf"),
                                                  attrib={etree.QName(xmlns.rdf, "resource"): elem.uri})
                    new_elem.append(subclass_node)

            # disjointWith
            if c.disjointWith is not None and len(c.disjointWith) > 0:
                for elem in c.disjointWith:
                    disjoint_node = etree.Element(etree.QName(xmlns.rdfs, "disjointWith"),
                                                  attrib={etree.QName(xmlns.rdf, "resource"): elem.uri})
                    new_elem.append(disjoint_node)

            # restriction
            if c.restrictions is not None and len(c.restrictions) > 0:
                for elem in c.restrictions:
                    restriction_node = etree.Element(etree.QName(xmlns.owl, "Restriction"))
                    if elem.onProperty is not None:
                        new_prop_node = etree.Element(etree.QName(xmlns.owl, "onProperty"),
                                                      attrib={etree.QName(xmlns.rdf, "resource"): elem.onProperty.uri})
                        restriction_node.append(new_prop_node)
                    if elem.minCardinality is not None:
                        new_min_card_node = etree.Element(etree.QName(xmlns.owl, "minCardinality"),
                                                      attrib={etree.QName(xmlns.rdf, "resource"): elem.onProperty.uri})
                        restriction_node.append(new_min_card_node)
                    new_elem.append(restriction_node)

        rdf_xml_root.append(new_elem)

    file_to_write.write(etree.tostring(rdf_xml_root, encoding='unicode', pretty_print=True))