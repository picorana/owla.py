from monet.classes import *
from monet.classes import OWLClass
from pprint import pprint
import json


def load_jsonld(filepath, auto_add = True):
    result = Ontology()

    document = json.load(open(filepath, "r"))

    for elem in document:

        # classes
        if elem["@type"][0].split("#")[1] == "Class":
            if "_:genid" not in elem["@id"]:
                new_class = OWLClass(uri=elem["@id"])
                for key in elem:

                    # comment
                    if "#" in key and key.split("#")[1] == "comment":
                        new_class.comment = elem[key][0]["@value"]

                    # label
                    elif "#" in key and key.split("#")[1] == "label":
                        new_class.label = elem[key][0]["@value"]

                    # subClassOf
                    elif "#" in key and key.split("#")[1] == "subClassOf":
                        if result.has_class(uri=elem[key][0]["@id"]):
                            new_class.subClassOf.add(result.get_class(uri=elem[key][0]["@id"]))
                        elif auto_add:
                            new_subclass_class = OWLClass(uri=elem[key][0]["@id"])
                            new_class.subClassOf.add(new_subclass_class)
                            result.add_class(new_subclass_class)

                    # disjointWith
                    elif "#" in key and key.split("#")[1] == "disjointWith":
                        if result.has_class(uri=elem[key][0]["@id"]):
                            new_class.disjointWith.add(result.get_class(uri=elem[key][0]["@id"]))
                        elif auto_add:
                            new_disjoint_class = OWLClass(uri=elem[key][0]["@id"])
                            new_class.disjointWith.add(new_disjoint_class)
                            result.add_class(new_disjoint_class)

                # add the class to the ontology
                if result.has_class(uri=elem["@id"]):
                    prev_class = result.get_class(uri=elem["@id"])
                    prev_class = new_class
                else:
                    result.add_class(new_class)



    return result
