import re

def check_answer(output: str, ground_truth: dict) -> bool:

    assert ground_truth["style"] == "1a3orn"
    correct_answer = ground_truth["answer"]

    
    if "<answer>...</answer>" in output:
        output = output.split("<answer>...</answer>")[1]

    # Extract answer from output
    try:
        start_tag = "<answer>"
        end_tag = "</answer>"
        start_idx = output.find(start_tag) + len(start_tag)
        end_idx = output.find(end_tag)
        if start_idx == -1 or end_idx == -1:
            return False
        extracted_answer = output[start_idx:end_idx].strip()
    except:
        return False

    # Try different evaluation methods
    def attempt_eval(extracted_answer, correct_answer):
        try:
            if extracted_answer == correct_answer:
                return True

            eval_extracted = eval(extracted_answer)
            eval_correct = eval(correct_answer)
            
            # Handle numeric comparisons with some tolerance
            if isinstance(eval_extracted, (int, float)) and isinstance(eval_correct, (int, float)):
                return abs(eval_extracted - eval_correct) < 1e-6
            
            # Handle list/tuple comparisons
            if isinstance(eval_extracted, (list, tuple)) and isinstance(eval_correct, (list, tuple)):
                return list(eval_extracted) == list(eval_correct)
            
            # Direct comparison of evaluated expressions
            return eval_extracted == eval_correct
            
        except:
            # If evaluation fails, fall back to string comparison
            return False

    # strip and lower case
    extracted_answer = extracted_answer.strip().lower()
    correct_answer = correct_answer.strip().lower()

    if attempt_eval(extracted_answer, correct_answer):
        return True

    # remove $ and ,
    extracted_answer = extracted_answer.replace("$", "").replace(",", "")
    correct_answer = correct_answer.replace("$", "").replace(",", "")

    if attempt_eval(extracted_answer, correct_answer):
        return True

    # remove all non-digit characters
    extracted_answer = re.sub(r'[^0-9]', '', extracted_answer)
    correct_answer = re.sub(r'[^0-9]', '', correct_answer)

    # if the length < 2, then return false
    if len(extracted_answer) < 2 or len(correct_answer) < 2:
        return False

    if attempt_eval(extracted_answer, correct_answer):
        return True

    return False