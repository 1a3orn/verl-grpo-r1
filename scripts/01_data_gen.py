# Implementing
# https://verl.readthedocs.io/en/latest/preparation/prepare_data.html
import json
import pandas as pd
import argparse

from check_answer import check_answer

def handle_files(read_file, write_file):

    with open(read_file, "r") as f:
        data = json.load(f)

    converted = []
    for item in data:

        question_str = item["question"]
        answer_str = item["answer"]

        # Append some instructions about <think> and <answer>
        addition = (
            "First, please think about how to get the right answer inside <think>...</think> tags. "
            "Then write your answer inside <answer>...</answer> tags. "
            "Put only the answer in the <answer>...</answer> tags, no other text."
        )
        full_prompt = f"{question_str} {addition}"

        converted.append({
            "data_source": "1a3orn",
            "prompt": [
                {"role": "system", "content": "You are a helpful assistant, that thinks carefully before answering."},
                {"role": "user", "content": full_prompt}
            ],
            "prompt_text": full_prompt,
            "ability": "1a3orn",
            "reward_model": {
                "style": "1a3orn",
                "ground_truth": {
                    "answer": answer_str,
                    "style": "1a3orn"
                }
            }
        })

    # Check that all match format here
    print("Two Examples  of output file:")

    for item in converted:
        assert type(item["data_source"]) == str
        assert type(item["prompt"]) == list
        assert type(item["prompt"][0]) == dict
        assert type(item["prompt"][0]["role"]) == str
        assert type(item["prompt"][0]["content"]) == str
        assert type(item["prompt"][1]) == dict
        assert type(item["prompt"][1]["role"]) == str
        assert type(item["prompt"][1]["content"]) == str
        assert type(item["prompt_text"]) == str
        assert type(item["ability"]) == str
        assert type(item["reward_model"]) == dict
        assert type(item["reward_model"]["style"]) == str
        assert type(item["reward_model"]["ground_truth"]) == dict

        # Check answer with blank is false
        assert not check_answer("", item["reward_model"]["ground_truth"])
        assert not check_answer("<answer></answer>", item["reward_model"]["ground_truth"])
        assert not check_answer("<answer>disregard</answer>", item["reward_model"]["ground_truth"])
        assert not check_answer(f"<answer>{item['reward_model']['ground_truth']}</answer>", item["reward_model"]["ground_truth"])
    
    df = pd.DataFrame(converted)
    df.to_parquet(write_file)

    print(f"Created {len(converted)} output files")

def main():
    files = [
       ("./intermediate_data/geography_train_questions.json", "all_geography_train.parquet"),
       ("./intermediate_data/geography_validation_questions.json", "all_geography_test.parquet"),
       ("./intermediate_data/gsm8k_train_questions.json", "all_gsm8k_train.parquet"),
       ("./intermediate_data/gsm8k_validation_questions.json", "all_gsm8k_test.parquet"),
       ("./intermediate_data/trash_math_train_questions.json", "all_trash_math_train.parquet"),
       ("./intermediate_data/trash_math_validation_questions.json", "all_trash_math_test.parquet"),
       ("./intermediate_data/zebralogic_train_questions.json", "all_zebralogic_train.parquet"),
       ("./intermediate_data/zebralogic_validation_questions.json", "all_zebralogic_test.parquet"),
    ]

    for file in files:
        handle_files(file[0], file[1])

if __name__ == "__main__":
    main()

