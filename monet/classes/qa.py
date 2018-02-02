from monet.constants import *

class QA_set():
    """
    Class to store Question/Answer sets
    """

    question = None
    answer = None

    def __init__(self, question=None, answer=None):
        self.question = Question(question)
        self.answer = Answer(answer)

    def __str__(self):
        return str(self.question) + "\n" + str(self.answer)


class Question():
    """
    Class to store a question
    """

    question = None
    type = None

    def __init__(self, question=None):
        self.question = question

    def __str__(self):
        return self.question

    def detect_type(self):
        """
        Detects the type of a question: open-ended or closed-ended
        """

        # todo:
        # what if questions are more than one in one line?

        if self.question is None or self.question == "":
            raise ValueError("Question field is empty")

        if len(self.question.split(" ")) <= 1:
            raise ValueError("Question too short")

        words = self.question.lower().split(" ")

        if words[0] in AUX_VERBS or words[0] in BE_VERBS:
            if words[0] in BE_VERBS and "or" in words:
                self.type = "open-ended"
            elif "anyone" in words or "anybody" in words:
                self.type = "open-ended"
            else:
                self.type = "closed-ended"
        else:
            self.type = "open-ended"


class Answer():
    """
    Class to store an answer
    """

    answer = None

    def __init__(self, answer=None):
        self.answer = answer

    def __str__(self):
        return self.answer
