QA_TEST_PATH = "/home/rana/Amazon_data/qa_datasets/qa_Cell_Phones_and_Accessories.json"
QA_PATH = "/home/rana/Amazon_data/questions"
TEST_ONTOLOGY_FILEPATH="/home/rana/mONET/resources/people.rdf"
MOCKS_FILEPATH="./mocks/"

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

rdf_head = '<?xml version="1.0"?>' \
           '<rdf:RDF xmlns="http://owl.man.ac.uk/2006/07/sssw/people#"' \
           'xml:base="http://owl.man.ac.uk/2006/07/sssw/people"' \
           'xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"' \
           'xmlns:owl="http://www.w3.org/2002/07/owl#"' \
           'xmlns:xml="http://www.w3.org/XML/1998/namespace"' \
           'xmlns:xsd="http://www.w3.org/2001/XMLSchema#"' \
           'xmlns:ns0="http://owl.man.ac.uk/2006/07/sssw/people#"' \
           'xmlns:rdfs="http://www.w3.org/2000/01/rdf-schema#">'

rdf_tail = '</rdf:RDF>'