from .rdf_xml_parser import *


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