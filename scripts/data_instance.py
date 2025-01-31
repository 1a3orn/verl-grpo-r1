import re

def is_answer_correct(answer_attempt: str, target: int, available_numbers: list):

        # If answer_attempt includes the <answer>10 + 22 - 9</answer>.
        # from the example, then get rid of everything before it

        # Means we won't get right answer for 10 + 22 - 9, oh well
        if "<answer>10 + 22 - 9</answer>." in answer_attempt:
            answer_attempt = answer_attempt.split("<answer>10 + 22 - 9</answer>.")[1]

        # First, find everything wrapped inside <answer> </answer> tags,
        # if they are there.
        answer_contents = re.findall(r'<answer>(.*?)</answer>', answer_attempt)
        if len(answer_contents) > 0:
            answer = answer_contents[0]
        else:
            answer = None

        if not answer:
            return None

        # IF the contents of the answer has a = within it
        # then split and take the longest of the split 
        # elements
        if "=" in answer:
            answer = max(answer.split("="), key=len)

        try:
            # Second, check that the answer comes to the correct target
            total = eval(answer)
            if total != target:
                return False

            # Third, make sure that we only used numbers in available_numbers once
            numbers_used = [abs(float(x)) for x in re.findall(r'-?\d*\.?\d+', answer)]
            
            numbers_used_set = set(numbers_used)
            if len(numbers_used_set) != len(numbers_used):
                return False

            # Fourth, make sure that we only used numbers in available_numbers
            numbers_available = set([abs(float(x)) for x in available_numbers])
            if not numbers_used_set.issubset(numbers_available):
                return False

            return True

        except Exception as e:
            return False

        return True

class DataInstance:
    def __init__(self, data):
        self.data = data

    def __str__(self):
        return f"Instance(data={self.data})"

    def system_prompt(self):
        first = "A conversation between User and Assistant. The user asks a question, and the assistant solves it. "
        second = "The assistant first thinks about the reasoning process in its mind and then provides the user with the answer."
        return first + second

    def user_question(self):
        third = f"Using the numbers {self.data['numbers_available']}, create an equation that equals {self.data['target']}. "
        fourth = "You can use operations + and -, i.e, addition, subtraction, and making a number negative. "
        fifth = "Each number may be used once, or not at all. "
        sixth = "Show your work in <think> . . . </think> tags. Return the final answer in <answer> . . . </answer> tags, "
        seventh = f"for example <answer>10 + 22 - 9</answer>."
        return third + fourth + fifth + sixth + seventh

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
            self.data["numbers_available"]
        )

def test():
    data = {
        "target": 10,
        "numbers_available": [110,100,20,30]
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


