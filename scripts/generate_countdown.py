import json
from typing import List, Callable, Tuple
from random import randint, seed
import random

from const import DATA_SOURCE_PREFIX
from countdown_data_instance import CountdownDataInstance

def generate_countdown_data_one(
    num_numbers_range: Tuple[int, int],
    numbers_range: Tuple[int, int],
    randomize_phrasing: bool = True,
    use_max_numbers: bool = False,
):
    """
    Generate a single test data sample, where you are guaranteed 
    to be able to have a to reach the target numbers using
    the permitted operations.
    """
    
    # How many numbers are available?
    num_numbers = randint(num_numbers_range[0], num_numbers_range[1])

    # Generate the numbers available (guaranteed unique)
    numbers_available = random.sample(range(numbers_range[0], numbers_range[1] + 1), num_numbers)

    # Select between 2 and len(numbers) numbers to be used to make the target
    if not use_max_numbers:
        num_numbers_to_use = random.randint(2, len(numbers_available))
    else:
        num_numbers_to_use = len(numbers_available)
    numbers_to_use = random.sample(numbers_available, num_numbers_to_use)

    # Randomly flip the sign of some of the numbers
    equation_parts = []
    for i in range(len(numbers_to_use)):
        if random.random() < 0.4:
            equation_parts.append(-numbers_to_use[i])
        else:
            equation_parts.append(numbers_to_use[i])
    # Generate the target
    target = sum(equation_parts)

    ground_truth = {
        "style": "countdown",
        "numbers": numbers_available,
        "target": target,

        "numbers_to_use": numbers_to_use,
        "equation_parts": equation_parts,
    }

    d = CountdownDataInstance(ground_truth, randomize_phrasing)

    return {
        "data_source": "1a3orn_countdown",
        "prompt": d.question_text_messages(),
        "prompt_text": d.question_text_base(),
        "ability": "math",
        "reward_model": {
            "style": "countdown",
            "ground_truth": ground_truth
        }
    }
