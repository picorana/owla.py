import os
from lxml import etree
full_dir = os.path.dirname(__file__)

QA_TEST_PATH = "/home/rana/Amazon_data/qa_datasets/qa_Cell_Phones_and_Accessories.json"
QA_PATH = "/home/rana/Amazon_data/questions"
TEST_ONTOLOGY_FILEPATH = "/home/rana/mONET/resources/people.rdf"
MOCKS_FILEPATH = os.path.join(full_dir, 'tests/mocks/')
OUTPUT_PATH = "test_output.rdf"

BE_VERBS = {"am", "are", "is", "was", "were", "being", "been"}

AUX_VERBS = {"can", "could", "dare", "do", "does", "did", "have", "has", "had", "having",
             "may", "might", "must", "need", "ought", "shall", "should", "will", "would"}

carriers = {'boost mobile', 'lycamobile', 'telcel', 'cricket', 'virgin mobile', 'h2o', 'telstra', 'at&t', 'movistar',
            'tracfone', 'tracphone', 'sprint', 'verizon', 'claro', 'tmobile', 't-mobile', 'metropcs', 'metro pcs',
            't mobile'}
technologies = {'micro sim', 'bluetooth', 'qi wireless', 'ir sensor', '4g', 'lte', '3g', 'cdma', 'gsm', 'wi-fi', 'wifi',
                'hotspot', 'hot spot', 'nfc', 'dual sim', 'two sim'}
operative_systems = {'android', 'android 8', 'android 7', 'android 6', 'lollipop', 'froyo', 'marshmallow', 'oreo',
                     'nougat', 'jellybean', 'gingerbread', 'ice cream sandwich'}
legal = {'warranty', 'warranties', 'unlocked'}

class xmlns:
    rdf = "http://www.w3.org/1999/02/22-rdf-syntax-ns#"
    owl = "http://www.w3.org/2002/07/owl#"
    xml = "http://www.w3.org/XML/1998/namespace"
    xsd = "http://www.w3.org/2001/XMLSchema#"
    rdfs = "http://www.w3.org/2000/01/rdf-schema#"

xml_head = '<?xml version="1.0"?>'

rdf_xml_type_map = {
    "OWLClass":"Class",
    "NamedIndividual":"NamedIndividual",
    "ObjectProperty":"ObjectProperty",
    "DataProperty":"DataProperty"
}