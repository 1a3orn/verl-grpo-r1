import random

def system_prompt():
    first = "A conversation between User and Assistant. The user asks a question, and the assistant solves it. "
    second = "The assistant first thinks about the reasoning process in its mind and then provides the user with the answer."
    return first + second

def user_question(numbers_to_sort):
    first = f"Your task is to sort the numbers {numbers_to_sort} into an ascending order, i.e., from lowest to highest. "
    second = "Then, drop every other number from the array, i.e., the 2nd, 4th, 6th, etc. numbers. "
    third = "Finally, return the remaining list."
    fourth = "Show your work in <think> . . . </think> tags. Return the final answer in <answer> . . . </answer> tags, "
    fifth = "for example <answer>[1, 3, 5, 7]</answer>."
    return first + second + third + fourth + fifth

def as_messages(numbers_to_sort):
    return [
        {"role": "developer", "content": system_prompt()},
        {"role": "user", "content": user_question(numbers_to_sort)}
    ]

def as_prompt_text(numbers_to_sort):
    return system_prompt() + "\nUser: " + user_question(numbers_to_sort) + "\nAssistant: <think> "

def generate_sort_odd_data_one(
    min_numbers: int,
    max_numbers: int,
):

    data_source = f"1a3orn_sort_odd"
    numbers_to_sort = random.sample(range(1, 100 + 1), k=random.randint(min_numbers, max_numbers))
    sorted_numbers = sorted(numbers_to_sort)
    every_other_number = [x for i, x in enumerate(sorted_numbers) if i % 2 == 0]

    return {
        "data_source": data_source,
        "prompt": as_messages(numbers_to_sort),
        "prompt_text": as_prompt_text(numbers_to_sort),
        "ability": "math",
        "reward_model": {
            "style": "sort_odd",
            "ground_truth": {
                "style": "sort_odd",
                "target": every_other_number,
                "numbers": numbers_to_sort
            }
        }
    }