
from nose.tools import (assert_equal, assert_not_equal,
                        assert_true, assert_false, assert_raises)

from monet.classes import *

print("Running tests:")

try: import nose
except ImportError:
    raise ImportError("nose package required to run tests")

def test1():
    assert_true(1==1)

def test_qa_set_question_init():
    qa = QA_set("hello", "goodbye")
    assert_equal(str(qa.question), "hello")
    assert_equal(str(qa.answer), "goodbye")

def test_question_detect_type():
    question = Question("")
    assert_raises(ValueError, question.detect_type)

    question = Question("Hello")
    assert_raises(ValueError, question.detect_type)

    question = Question("Does it work")
    question.detect_type()
    assert_equal(question.type, "closed-ended")

    question = Question("Is he married or not")
    question.detect_type()
    assert_equal(question.type, "open-ended")

def test_ontology():
    onto = Ontology()
    assert_equal(onto.classes.pop().name, "owl:Thing")

    ontoclass = OntologyClass("")
    ontoclass.add_property(Property("has_color"))
    assert_true(ontoclass.properties, {Property("has_color")})

def test_properties():
    prop = DataProperty("test", str)
    assert_equal(prop.name, "test")
    assert_equal(prop.mimetype, str)

    prop = ObjectProperty("test")
    assert_equal(prop.name, "test")

def test_extract_from_question():

    import monet.extract

    assert_equal(monet.extract.property_from_question("Does it work in Argentina?"), "argentina")
