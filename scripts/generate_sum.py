import random

def system_prompt():
    first = "A conversation between User and Assistant. The user asks a question, and the assistant solves it. "
    second = "The assistant first thinks about the reasoning process in its mind and then provides the user with the answer."
    return first + second

def user_question(numbers_to_sum):
    first = f"Your task is to sum the numbers {numbers_to_sum}. "
    second = "Show your work in <think> . . . </think> tags. Return the final answer in <answer> . . . </answer> tags, "
    third = "for example <answer>234</answer>."
    return first + second + third

def as_messages(numbers_to_sum):
    return [
        {"role": "developer", "content": system_prompt()},
        {"role": "user", "content": user_question(numbers_to_sum)}
    ]

def as_prompt_text(numbers_to_sum):
    return system_prompt() + "\nUser: " + user_question(numbers_to_sum) + "\nAssistant: <think> "

def generate_sum_data_one(
    min_numbers: int,
    max_numbers: int,
):

    numbers_to_sum = random.sample(range(1, 100 + 1), k=random.randint(min_numbers, max_numbers))
    sum_of_numbers = sum(numbers_to_sum)

    return {
        "data_source": f"1a3orn_sum",
        "prompt": as_messages(numbers_to_sum),
        "prompt_text": as_prompt_text(numbers_to_sum),
        "ability": "math",
        "reward_model": {
            "style": "sum",
            "ground_truth": {
                "style": "sum",
                "target": sum_of_numbers,
            }
        }
    }