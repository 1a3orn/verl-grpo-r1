import re
import random

class CountdownDataInstance:
    def __init__(self, data, randomize_phrasing=False):
        self.data = data
        self.randomize_phrasing = randomize_phrasing

    def __str__(self):
        return f"Instance(data={self.data})"

    def system_prompt(self):
        first = "A conversation between User and Assistant. The user asks a question, and the assistant solves it. "
        second = "The assistant first thinks about the reasoning process in its mind and then provides the user with the answer."
        return first + second

    def user_question(self):
        if not self.randomize_phrasing:
            third = f"Using the numbers {self.data['numbers']}, create an equation that equals {self.data['target']}. "
            fourth = "You can use operations + and -, i.e, addition, subtraction, and making a number negative. "
            fifth = "Each number may be used once, or not at all. "
            sixth = "Show your work in <think> . . . </think> tags. Return the final answer in <answer> . . . </answer> tags, "
            seventh = f"for example <answer>10 + 22 - 9</answer>."
            return third + fourth + fifth + sixth + seventh
        else:
            third = random.choice([
                f"Using the numbers {self.data['numbers']}, create an equation that equals {self.data['target']}. ",
                f"Make an equation that equals {self.data['target']}, with the numbers {self.data['numbers']}. ",
                f"You have the numbers {self.data['numbers']} to use. Make an equation with them that equals {self.data['target']}. ",
                f"The numbers {self.data['numbers']} are available to use. Use them to make an equation that equals {self.data['target']}. ",
            ])
            fourth = random.choice([
                "You can use operations + and -, i.e, addition, subtraction, and making a number negative. ",
                "You can addition, subtraction, and making a number negative, i.e., +, -, and -x. ",
                "Operations allowed in the equation are +, -, and -x, i.e., addition, subtraction, and making a number negative. ",
            ])
            fifth = random.choice([
                "Each number may be used once, or not at all. ",
                "Each number may be used at most once. You may also choose not to use any particular number. ",
                "You may use each number at most once, but may leave out any particular number. ",
            ])
            sixth = random.choice([
                "Show your work in <think> . . . </think> tags. Return the final answer in <answer> . . . </answer> tags, for example <answer>10 + 22 - 9</answer>.",
                "Think through the problem step by step inside <think> . . . </think> tags. Return the final equation in <answer> . . . </answer> tags, for example <answer>10 + 22 - 9</answer>.",
                "First consider the problem carefully inside <think> . . . </think> tags. The final equation should go in <answer> . . . </answer> tags, i.e., <answer>10 + 22 - 9</answer>.",
                "Be sure to first show your work in <think> . . . </think> tags. The final equation should go inside paired <answer> tags."
            ])
            return third + fourth + fifth + sixth

    def question_text_base(self):
        first = self.system_prompt()
        second = "\nUser: " + self.user_question()
        third = "\nAssistant: Let me solve this step by step. <think> "
        return first + second + third

    def question_text_messages(self):
        messages = [
            {"role": "developer", "content": self.system_prompt()},
            {"role": "user", "content": self.user_question()}
        ]
        return messages

    def is_answer_correct(self, answer_attempt: str):
        return is_answer_correct(
            answer_attempt,
            self.data["target"],
            self.data["numbers"]
        )

def test():
    data = {
        "target": 10,
        "numbers": [110,100,20,30]
    }
    instance = DataInstance(data)
    assert not instance.is_answer_correct("10")
    assert not instance.is_answer_correct("<answer>10</answer>")
    assert not instance.is_answer_correct("<answer>5 + 5</answer>")
    assert instance.is_answer_correct("<answer>30 - 20</answer>")
    assert instance.is_answer_correct("<answer>110 - 100</answer>")
    assert instance.is_answer_correct("<answer>110.0 - 100.0</answer>")
    assert instance.is_answer_correct("<answer>-100 + 110</answer>")
    assert instance.is_answer_correct("<answer>-(100 - 110)</answer>")
    assert instance.is_answer_correct("<answer>-(-110 + 100)</answer>")
    assert instance.is_answer_correct("<answer>110 - 100 = 10</answer>")
    assert instance.is_answer_correct("<answer>10 = 30 - 20</answer>")
    assert instance.is_answer_correct("<answer>-(-110 + 100) = 10</answer>")
    assert not instance.is_answer_correct("<answer>110 - 100 + 20 - 20</answer>")
if __name__ == "__main__":
    test()


