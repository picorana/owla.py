
import sys
if sys.version_info[:2] < (2, 7):
    m = "Python 2.7 or more required (%d.%d detected)."
    raise ImportError(m % sys.version_info[:2])
del sys

from monet.classes import *
from monet.extract import *
from monet.constants import *

load_ontology_from_file(TEST_ONTOLOGY_FILEPATH)


