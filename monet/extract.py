from monet.constants import *
from monet.classes import *

import spacy

# todo:
# detect if there are negations in questions or answers
# detect type of answer
# detect if question is open or closed


def properties_from_question(question):

    result = set()

    nlp = spacy.load('en')

    doc = nlp(question)

    # CARRIERS
    if any(word in question.lower() for word in carriers):
        for word in carriers:
            if word in question.lower():
                result.add(DataProperty(label="carrier_supported", value=word))

    # SUPPORTED TECHNOLOGIES
    if any(word in question.lower() for word in technologies):
        for word in technologies:
            if word in question.lower():
                result.add(DataProperty(label="technology_supported", value=word))

    # LOCATIONS
    if any(ent.label_ == "GPE" or ent.label_ == "LOC" for ent in doc.ents):

        if 'made' in question.lower() or 'manufactured' in question.lower():
            for ent in doc.ents:
                if ent.label_ == "GPE" or ent.label_ == "LOC":
                    loc = ent.string.strip().lower()
                    result.add(DataProperty(label="made_in", value=loc))

        else:
            for ent in doc.ents:
                if ent.label_ == "GPE" or ent.label_ == "LOC":
                    loc = ent.string.strip().lower()
                    result.add(DataProperty(label="location", value=loc))

    if any(ent.label_ == "ORG" for ent in doc.ents):
        for ent in doc.ents:
            if ent.label_ == "ORG":
                loc = ent.string.strip().lower()
                result.add(DataProperty(label="org", value=loc))

    if any(ent.label_ == "LANGUAGE" for ent in doc.ents):
        for ent in doc.ents:
            if ent.label_ == "LANGUAGE":
                loc = ent.string.strip().lower()
                result.add(DataProperty(label="language", value=loc))

    return result


