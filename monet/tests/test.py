
from nose.tools import (assert_equal, assert_not_equal,
                        assert_true, assert_false, assert_raises)

from monet.classes import *
import gc

print("Running tests:")

try:
    import nose
except ImportError:
    raise ImportError("nose package required to run tests")


def test1():
    assert_true(1 == 1)


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


def test_properties():
    prop = DataProperty(label="test", mimetype=str)
    assert_equal(prop.label, "test")
    assert_equal(prop.mimetype, str)

    prop = ObjectProperty(label="test")
    assert_equal(prop.label, "test")


def test_extract_from_question():

    import monet.extract

    assert_equal(monet.extract.properties_from_question("Does it work in Argentina?").pop().value,
                 DataProperty(label="location", value="argentina").value)


def test_ontology_class_add_property():
    ontoclass = OWLClass("")
    ontoclass.add_property(OWLProperty("has_color"))
    assert_true(ontoclass.properties, {OWLProperty("has_color")})


def test_ontology_has_class():
    onto = Ontology()
    onto.add_class(OWLClass(label="test"))
    assert_true(onto.has_class(label="test"))


def test_ontology_add_same_class():
    onto = Ontology()
    onto.add_class(OWLClass(label="test"))
    assert_raises(RuntimeError, onto.add_class(OWLClass(label="test")))


def test_ontology_get_class():
    onto = Ontology()
    c = OWLClass(label="test")
    onto.add_class(c)
    assert_equal(onto.get_class(label="test"), c)


def test_ontology_rdf_xml_single_class():
    onto = load_ontology_from_file(MOCKS_FILEPATH + "single_class.rdf")
    assert_equal(onto.about, "http://www.semanticweb.org/ontologies/2018/1/untitled-ontology-9")

    assert_equal(onto.classes.pop().about, "http://www.semanticweb.org/ontologies/2018/1/untitled-ontology-9#test")

def test_ontology_rdf_xml_data_object_properties():
    onto = load_ontology_from_file(MOCKS_FILEPATH + "data_object_property.rdf")

    print(onto)

    assert_equal(onto.classes.pop().about, "http://www.semanticweb.org/ontologies/2018/1/untitled-ontology-9#test")
