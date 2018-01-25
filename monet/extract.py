from monet.constants import *
from monet.classes import *

import spacy


def property_from_question(question):

    nlp = spacy.load('en')

    doc = nlp(question)

    if any(ent.label_ == "GPE" or ent.label_ == "LOC" for ent in doc.ents):
        for ent in doc.ents:
            if ent.label_ == "GPE" or ent.label_ == "LOC":
                loc = ent.string.strip().lower()
                return loc

