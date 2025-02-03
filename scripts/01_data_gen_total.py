# Implementing
# https://verl.readthedocs.io/en/latest/preparation/prepare_data.html
import json
import pandas as pd
import argparse

from check_answer import is_answer_correct
from generate_sum import generate_sum_data_one
from generate_countdown import generate_countdown_data_one
from generate_sort_odd import generate_sort_odd_data_one

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output_file_prefix", type=str, required=True)
    args = parser.parse_args()  

    output_files = [
        {
            "data_source": "1a3orn_train",
            "file_name": f"{args.output_file_prefix}_train.parquet",
            "generate_fn": lambda: [generate_countdown_data_one(
                num_numbers_range=(3, 5),
                numbers_range=(1, 100),
                randomize_phrasing=True
            ) for _ in range(100000)]
        },
        {
            "data_source": "1a3orn_test",
            "file_name": f"{args.output_file_prefix}_test.parquet",
            "generate_fn": lambda: [ generate_countdown_data_one(
                num_numbers_range=(3, 5),
                numbers_range=(1, 100),
                randomize_phrasing=True
            ) for _ in range(50)]
        },
        {
            "data_source": "1a3orn_test_not_random",
            "file_name": f"{args.output_file_prefix}_test.parquet",
            "generate_fn": lambda: [ generate_countdown_data_one(
                num_numbers_range=(3, 5),
                numbers_range=(1, 100),
                randomize_phrasing=False,
            ) for _ in range(50)]
        },
        {
            "data_source": "1a3orn_off_six",
            "file_name": f"{args.output_file_prefix}_off_six.parquet",
            "generate_fn": lambda: [ generate_countdown_data_one(
                num_numbers_range=(6, 6),
                numbers_range=(1, 100),
                use_max_numbers=True
            ) for _ in range(50)]
        },
        {
            "data_source": "1a3orn_off_seven",
            "file_name": f"{args.output_file_prefix}_off_seven.parquet",
            "generate_fn": lambda: [ generate_countdown_data_one(
                num_numbers_range=(7, 7),
                numbers_range=(1, 100),
                use_max_numbers=True
            ) for _ in range(50)]
        },
        {
            "data_source": "1a3orn_sort_odd",
            "file_name": f"{args.output_file_prefix}_sort_odd.parquet",
            "generate_fn": lambda: [ generate_sort_odd_data_one(
                min_numbers=4,
                max_numbers=10
            ) for _ in range(50)]
        },
        {
            "data_source": "1a3orn_sum",
            "file_name": f"{args.output_file_prefix}_sum.parquet",
            "generate_fn": lambda: [ generate_sum_data_one(
                min_numbers=4,
                max_numbers=7
            ) for _ in range(50)]
        }
    ]
    
    created_output_files = []
    for output_file in output_files:
        data = output_file["generate_fn"]()
        for item in data:
            item["data_source"] = output_file["data_source"]
        created_output_files.append(data)

    # Check that all match format here
    for lst in created_output_files:
        print("Two Examples  of output file:")
        print(json.dumps(lst[0], indent=4))
        print(json.dumps(lst[1], indent=4))
        for item in lst:
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
            assert not is_answer_correct("", item["reward_model"]["ground_truth"])
            assert not is_answer_correct("<answer></answer>", item["reward_model"]["ground_truth"])
            assert not is_answer_correct("<answer>disregard</answer>", item["reward_model"]["ground_truth"])
            assert not is_answer_correct(f"<answer>{item['reward_model']['ground_truth']}</answer>", item["reward_model"]["ground_truth"])




    for i, output_file in enumerate(created_output_files):
        df = pd.DataFrame(output_file)
        df.to_parquet(output_files[i]["file_name"])

    print(f"Created {len(created_output_files)} output files")

if __name__ == "__main__":
    main()

