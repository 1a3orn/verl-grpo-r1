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

def compute_score(solution_str, ground_truth, method='strict', format_score=0., score=1.):

    if is_answer_correct(solution_str, ground_truth["target"], ground_truth["numbers"]):
        return score
    else:

        # If we have <answer>...</answer>, then it's 
        # at least formatted correctly
        answer_contents = re.findall(r'<answer>(.*?)</answer>', solution_str)
        if len(answer_contents) > 0:
            return format_score
        else:
            return 0

def tests():
    assert is_answer_correct("<answer>10 + 22 - 9</answer>", 23, [10, 22, 9]) == 1
    assert is_answer_correct("<answer>10 + 22</answer>", 23, [10, 22, 9]) == 0.1
