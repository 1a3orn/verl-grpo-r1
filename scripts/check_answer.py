import re

def is_answer_correct(answer_attempt: str, ground_truth: dict):
    if ground_truth["style"] == "countdown":
        return is_answer_correct_countdown(answer_attempt, ground_truth)
    elif ground_truth["style"] == "sort_odd":
        return is_answer_correct_sort_odd(answer_attempt, ground_truth)
    elif ground_truth["style"] == "sum":
        return is_answer_correct_find_sum(answer_attempt, ground_truth)
    else:
        raise ValueError(f"Unknown style: {ground_truth['style']}")


def is_answer_correct_find_sum(answer_attempt: str, ground_truth: dict):
    target = ground_truth["target"]

    # If answer_attempt includes the <answer>10 + 22 + 9</answer>.
    # from the example, then get rid of everything before it
    if "<answer>234</answer>." in answer_attempt:
        answer_attempt = answer_attempt.split("<answer>234</answer>.")[1]

    answer_contents = re.findall(r'<answer>(.*?)</answer>', answer_attempt)
    if len(answer_contents) > 0:
        answer = answer_contents[0]
    else:
        answer = None

    if not answer:
        return None

    try:
        answer = answer.strip()

        # Check hat answer is just a single number, including decimals
        if not re.match(r'^-?\d+\.?\d*$', answer):
            return False

        # eval answer
        answer = eval(answer)


        if answer != target:
            return False

        return True
    except Exception as e:
        return False

def is_answer_correct_sort_odd(answer_attempt: str, ground_truth: dict):
    target = ground_truth["target"]

    # If answer_attempt includes the <answer>[1, 3, 5, 7]</answer>.
    # from the example, then get rid of everything before it

    if "<answer>[1, 3, 5, 7]</answer>." in answer_attempt:
        answer_attempt = answer_attempt.split("<answer>[1, 3, 5, 7]</answer>.")[1]

    answer_contents = re.findall(r'<answer>(.*?)</answer>', answer_attempt)
    if len(answer_contents) > 0:
        answer = answer_contents[0]
    else:
        answer = None

    if not answer:
        return None

    try:
        answer = eval(answer.strip())
        
        # Check that the answer is a list
        if not isinstance(answer, list):
            return False

        # Check that the answer is a list of numbers
        if not all(isinstance(x, int) or isinstance(x, float) for x in answer):
            return False

        # Check length matches
        if len(answer) != len(target):
            return False

        # Check the numbers are the same at each spot
        for i in range(len(answer)):
            if answer[i] != target[i]:
                return False

        return True
    except Exception as e:
        return False


def is_answer_correct_countdown(answer_attempt: str, ground_truth: dict):

        target = ground_truth["target"]
        numbers = ground_truth["numbers"]

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
            #print(answer, total, target)
            if total != target:
                return False

            # Third, make sure that we only used numbers in available_numbers once
            numbers_used = [abs(float(x)) for x in re.findall(r'-?\d*\.?\d+', answer)]
            numbers_used_set = set(numbers_used)
            if len(numbers_used_set) != len(numbers_used):
                return False

            # Fourth, make sure that we only used numbers in available_numbers
            numbers_available = set([abs(float(x)) for x in numbers])
            if not numbers_used_set.issubset(numbers_available):
                #print("asdad", numbers_used_set, numbers_used)
                return False

            return True

        except Exception as e:
            return False

        return True

def test_sorted():
    ground_truth = {
        "style": "sort_odd",
        "target": [1, 3, 5, 7, 9],
        "numbers": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    }
    assert is_answer_correct("<answer>[1, 3, 5, 7, 9]</answer>.", ground_truth)
    assert is_answer_correct("<answer> [1.0, 3.0, 5, 7, 9] </answer>.", ground_truth)
    assert not is_answer_correct("<answer> [3.0, 1, 5, 7, 9] </answer>.", ground_truth)
    assert not is_answer_correct("<answer> [1, 3, 5, 7, 9, 11] </answer>.", ground_truth)
    assert not is_answer_correct("<answer> [1, 3, 5, 7, 8] </answer>.", ground_truth)

def test_countdown():
    ground_truth = {
        "style": "countdown",
        "target": 10,
        "numbers": [110,100,20,30]
    }
    assert not is_answer_correct("10", ground_truth)
    assert not is_answer_correct("<answer>10</answer>", ground_truth)
    assert not is_answer_correct("<answer>5 + 5</answer>", ground_truth)
    assert is_answer_correct("<answer>30 - 20</answer>", ground_truth)
    assert is_answer_correct("<answer>110 - 100</answer>", ground_truth)
    assert is_answer_correct("<answer>110.0 - 100.0</answer>", ground_truth)
    assert is_answer_correct("<answer>-100 + 110</answer>", ground_truth)
    assert is_answer_correct("<answer>-(100 - 110)</answer>", ground_truth)
    assert is_answer_correct("<answer>-(-110 + 100)</answer>", ground_truth)
    assert is_answer_correct("<answer>110 - 100 = 10</answer>", ground_truth)
    assert is_answer_correct("<answer>10 = 30 - 20</answer>", ground_truth)
    assert is_answer_correct("<answer>-(-110 + 100) = 10</answer>", ground_truth)
    assert not is_answer_correct("<answer>110 - 100 + 20 - 20</answer>", ground_truth)

def test_find_sum():
    ground_truth = {
        "style": "find_sum",
        "target": 100,
    }
    assert is_answer_correct("<answer> 100 </answer>", ground_truth)
    assert is_answer_correct("<answer> 100.0 </answer>", ground_truth)
    assert not is_answer_correct("<answer> 100.1</answer>", ground_truth)
    assert not is_answer_correct("<answer> 50 + 50</answer>", ground_truth)
    assert not is_answer_correct("<answer> 100 = 100.0</answer>", ground_truth)

def test():
    test_sorted()
    test_countdown()
    test_find_sum()

if __name__ == "__main__":
    test()