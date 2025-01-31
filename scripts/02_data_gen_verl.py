# Implementing
# https://verl.readthedocs.io/en/latest/preparation/prepare_data.html
#
#
# So, specifically making a data format that is compatible with verl
# where each bit of data has the fields
# - data_source (string)
# - prompt (a list of dicts with role and content)
# - ability (string)
# - reward_model (dict with style and ground_truth)
# - extra_info (dict with split and index)

# All this is saved as a parquet file.

import json
import pandas as pd
import argparse
from data_instance import DataInstance
from const import DATA_SOURCE_PREFIX, TRAIN, TEST, OFF_TARGET, OFF_SIX, OFF_SEVEN, OFF_EIGHT

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_file", type=str, required=True)
    parser.add_argument("--output_file_prefix", type=str, required=True)
    args = parser.parse_args()  
    # Load the input file which we assume will be a json
    # with the following fields:
    # - label: TRAIN | TEST | OFF_TARGET | OFF_SIX | OFF_SEVEN | OFF_EIGHT
    # - numbers_available: list of numbers
    # - numbers_to_use: list of numbers
    # - target: int
    # - equation_parts: list of numbers

    with open(args.input_file, 'r') as f:
        data = json.load(f)
    print(f"Loaded {len(data)} samples")

    for ds in data:
        assert ds["label"] in [TRAIN, TEST, OFF_TARGET, OFF_SIX, OFF_SEVEN, OFF_EIGHT]
        assert type(ds["numbers_available"]) == list
        assert all(isinstance(x, int) for x in ds["numbers_available"])
        assert type(ds["numbers_to_use"]) == list
        assert all(isinstance(x, int) for x in ds["numbers_to_use"])
        assert type(ds["target"]) == int
        assert type(ds["equation_parts"]) == list
        assert all(isinstance(x, int) for x in ds["equation_parts"])

    def make_map_fn(ds):
        d = DataInstance(ds)
        return {
            "data_source": DATA_SOURCE_PREFIX + "_" + ds["label"],
            "prompt": d.question_text_messages(),
            "prompt_text": d.question_text_base(),
            "ability": "countdown",
            "reward_model": {
                "style": "countdown",
                "ground_truth": {
                    "target": ds["target"],
                    "numbers": ds["numbers_available"]
                }
            }
        }

    # Define labels and their corresponding file suffixes
    labels = [TRAIN, TEST, OFF_TARGET, OFF_SIX, OFF_SEVEN, OFF_EIGHT]

    # Create dataframes and save to parquet in one loop
    for label in labels:
        print(f"Processing {label}")
        data_filtered = [make_map_fn(d) for d in data if label.lower() == d["label"].lower()]
        print(f"Filtered data length: {len(data_filtered)}")
        df = pd.DataFrame(data_filtered)
        df.to_parquet(f"{args.output_file_prefix}_{label}.parquet".lower())


if __name__ == "__main__":
    main()

