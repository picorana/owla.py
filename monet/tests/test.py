
from nose.tools import (assert_equal, assert_not_equal,
                        assert_true, assert_false, assert_raises)

from monet.classes import *

def run():
    try: import nose
    except ImportError:
        raise ImportError("nose package required to run tests")

    print("Running tests:")

    nose.run()

class Test():

    print("Running tests:")

    def test1(self):
        assert_true(1==1)

    def test_qa_set_question_init(self):
        qa = QA_set("hello", "goodbye")
        assert_equal(str(qa.question), "hello")
        assert_equal(str(qa.answer), "goodbye")

    def test_question_detect_type(self):
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

if __name__ == "__main__":
    run()