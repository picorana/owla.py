from .rdf_xml_writer import *


def write_ontology(ontology, output_path, syntax):

    if syntax == "rdf/xml":
        rdf_xml_write(ontology, output_path)
    else:
        raise RuntimeError("syntax style not recognized")
