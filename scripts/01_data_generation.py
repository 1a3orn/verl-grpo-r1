import json
from typing import List, Callable, Tuple
from random import randint, seed
import random

from const import TRAIN, TEST, OFF_TARGET, OFF_SIX, OFF_SEVEN, OFF_EIGHT

def generate_data(
    num_samples: int,
    num_numbers_range: Tuple[int, int],
    numbers_range: Tuple[int, int],
    # If exclusion callback is provided,
    # the generated data will not contain
    # any samples that satisfy the callback
    exclusion_callback: Callable[[int, List[int]], bool] = None,
):
    samples = []
    num_excluded = 0

    while len(samples) < num_samples:
        test_data = generate_test_data(num_numbers_range, numbers_range)
        if exclusion_callback is not None and exclusion_callback(test_data):
            num_excluded += 1
            continue
        samples.append(test_data)

    return samples

def generate_test_data(
    num_numbers_range: Tuple[int, int],
    numbers_range: Tuple[int, int],
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
    num_numbers_to_use = random.randint(2, len(numbers_available))
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

    return {
        "numbers_available": numbers_available,
        "numbers_to_use": numbers_to_use,
        "target": target,
        "equation_parts": equation_parts,
    }

BASE_NUM_NUMBERS_RANGE = (3, 5)
BASE_NUMBERS_RANGE = (1, 60)

def generate_on_domain_data(num_samples: int, seed_value: int):

    def exclusion_callback(test_data):
        # Exclue if the target is between 60 and 64
        if 60 <= test_data["target"] <= 68:
            print(f"Excluding -- target {test_data['target']}")
            return True

        return False

    return generate_data(num_samples, BASE_NUM_NUMBERS_RANGE, BASE_NUMBERS_RANGE, exclusion_callback)


def generate_off_domain_data_target(num_samples: int, seed_value: int):
    def exclusion_callback(test_data):
        if test_data["target"] < 60 or test_data["target"] > 68:
            return True
        return False
    return generate_data(num_samples, BASE_NUM_NUMBERS_RANGE, BASE_NUMBERS_RANGE, exclusion_callback)

if __name__ == "__main__":
    seed(1)

    """
    Generate 200,000 samples from the on domain
    data, which will be used to train the model
    """
    on_domain_train = generate_on_domain_data(100000, 1)
    for data in on_domain_train:
        assert data["target"] < 60 or data["target"] > 68

    on_domain_test = generate_on_domain_data(50, 2)

    """
    Generate 100 samples for EACH off domain category
    """
    # Target being between 60 and 68
    off_domain_target_data = generate_off_domain_data_target(50, 1)
    for data in off_domain_target_data:
        assert data["target"] >= 60 and data["target"] <= 68

    # Numbers available being 6, 7, or 8
    off_domain_six_available = generate_data(50, (6, 6), BASE_NUMBERS_RANGE, None)
    off_domain_seven_available = generate_data(50, (7, 7), BASE_NUMBERS_RANGE, None)
    off_domain_eight_available = generate_data(50, (8, 8), BASE_NUMBERS_RANGE, None)

    #
    """
    Join all the data together, with labels:
    - TRAIN: 190,000
    - TEST: 50
    - OFF_DOMAIN_TARGET: 50
    - OFF_DOMAIN_SIX_AVAILABLE: 50
    - OFF_DOMAIN_SEVEN_AVAILABLE: 50
    - OFF_DOMAIN_EIGHT_AVAILABLE: 50
    """

    train = [{"label": TRAIN, **data} for data in on_domain_train]
    test = [{"label": TEST, **data} for data in on_domain_test]
    off_domain_target = [{"label": OFF_TARGET, **data} for data in off_domain_target_data]
    off_domain_six = [{"label": OFF_SIX, **data} for data in off_domain_six_available]
    off_domain_seven = [{"label": OFF_SEVEN, **data} for data in off_domain_seven_available]
    off_domain_eight = [{"label": OFF_EIGHT, **data} for data in off_domain_eight_available]

    datas = train + test + off_domain_target + off_domain_six + off_domain_seven + off_domain_eight

    print(len(datas))

    with open("data.json", "w") as f:
        json.dump(datas, f, indent=4)

    #print(json.dumps(off_domain_available_nums_data, indent=4))


    #print(json.dumps(datas, indent=4))
