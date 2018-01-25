
import sys
if sys.version_info[:2] < (2, 7):
    m = "Python 2.7 or more required (%d.%d detected)."
    raise ImportError(m % sys.version_info[:2])
del sys

from monet.classes import *
from monet.extract import *
from monet.constants import *

import owlready2
import spacy
import pprint
import json
import os

# nlp = spacy.load('en')

"""
for i, elem in enumerate(os.listdir(QA_PATH)):
    if i == 2: break

    print(elem)

    item_characteristics_dict = {'asin': elem.split('.')[0]}

    for line in open(QA_PATH  + '/' + elem, 'r'):

        try:
            qa = json.loads(line)

            doc = nlp(qa['question'])

            found_at_least_one = False

            # CARRIERS
            if any(word in qa['question'].lower() for word in carriers):
                if 'carriers_supported' not in item_characteristics_dict: item_characteristics_dict[
                    'carriers_supported'] = {}

                for word in carriers:
                    if word in qa['question']:
                        if word not in item_characteristics_dict['carriers_supported']:
                            item_characteristics_dict['carriers_supported'][word] = []
                            item_characteristics_dict['carriers_supported'][word].append((qa['question'], qa['answer']))

                found_at_least_one = True

            # SUPPORTED TECHNOLOGIES
            if any(word in qa['question'].lower() for word in technologies):
                if 'technologies_supported' not in item_characteristics_dict: item_characteristics_dict[
                    'technologies_supported'] = {}

                for word in technologies:
                    if word in qa['question']:
                        if word not in item_characteristics_dict['technologies_supported']:
                            item_characteristics_dict['technologies_supported'][word] = []
                            item_characteristics_dict['technologies_supported'][word].append((qa['question'], qa['answer']))

                found_at_least_one = True

            # LOCATIONS
            if any(ent.label_ == "GPE" or ent.label_ == "LOC" for ent in doc.ents):

                found_at_least_one = True

                if 'made' in qa['question'].lower() or 'manufactured' in qa['question'].lower():
                    if 'made_in' not in item_characteristics_dict: item_characteristics_dict['made_in'] = {}

                    for ent in doc.ents:
                        if ent.label_ == "GPE" or ent.label_ == "LOC":
                            loc = ent.string.strip().lower()
                            if loc not in item_characteristics_dict['made_in']: item_characteristics_dict['made_in'][
                                loc] = []
                            item_characteristics_dict['made_in'][loc].append((qa['question'], qa['answer']))

                else:
                    if 'locations' not in item_characteristics_dict: item_characteristics_dict['locations'] = {}

                    for ent in doc.ents:
                        if ent.label_ == "GPE" or ent.label_ == "LOC":
                            loc = ent.string.strip().lower()
                            if loc not in item_characteristics_dict['locations']:
                                item_characteristics_dict['locations'][loc] = []
                                item_characteristics_dict['locations'][loc].append((qa['question'], qa['answer']))

            if any(ent.label_ == "ORG" for ent in doc.ents):

                found_at_least_one = True

                if 'orgs' not in item_characteristics_dict: item_characteristics_dict['orgs'] = {}

                for ent in doc.ents:
                    if ent.label_ == "ORG":
                        loc = ent.string.strip().lower()
                        if loc not in item_characteristics_dict['orgs']: item_characteristics_dict['orgs'][loc] = []
                        item_characteristics_dict['orgs'][loc].append((qa['question'], qa['answer']))

            if any(ent.label_ == "LANGUAGE" for ent in doc.ents):

                found_at_least_one = True

                if 'languages' not in item_characteristics_dict: item_characteristics_dict['languages'] = {}

                for ent in doc.ents:
                    if ent.label_ == "LANGUAGE":
                        loc = ent.string.strip().lower()
                        if loc not in item_characteristics_dict['languages']: item_characteristics_dict['languages'][
                            loc] = []
                        item_characteristics_dict['languages'][loc].append((qa['question'], qa['answer']))

            if not found_at_least_one:
                for ent in doc.ents:
                    print(qa['question'], ent, ent.label_)

        except Exception as e:
            print(e)

    item_chars.append(item_characteristics_dict)

pprint.pprint(item_chars)
"""




