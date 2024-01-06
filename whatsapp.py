import json
import re
import argparse

def clean_and_format(input_file, output_file):
    # Function to check if the line is the start of a new conversation
    def is_start_of_conversation(line):
        return bool(re.match(r'\[\d{1,2}/\d{1,2}/\d{2}, \d{1,2}:\d{2}:\d{2}\s[APM]{2}\]', line))

    # Function to remove the timestamp and replace newlines with \n
    def remove_timestamp_and_convert_newlines(line):
        if ']' in line:
            line = line.split(']', 1)[1]
        return line

    # Read the input file
    with open(input_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    # Process lines
    chunks = []
    current_chunk = ''
    for line in lines:
        line = remove_timestamp_and_convert_newlines(line)
        if is_start_of_conversation(line) and current_chunk:
            chunks.append(current_chunk.strip())
            current_chunk = line
        elif len(current_chunk) + len(line) < 2000:
            current_chunk += line + ' '
        else:
            chunks.append(current_chunk.strip())
            current_chunk = line

    if current_chunk:
        chunks.append(current_chunk.strip())

    # Write to a JSONL file
    with open(output_file, 'w', encoding='utf-8') as out_file:
        for chunk in chunks:
            json_record = json.dumps({"text": chunk})
            out_file.write(json_record + '\n')

def split_jsonl(input_file, test_file, validate_file, train_file, test_size=30, validate_size=30):
    with open(input_file, 'r') as infile:
        lines = infile.readlines()

    # Ensure there are enough lines to split as requested
    if len(lines) < test_size + validate_size:
        raise ValueError("Not enough data to split as requested.")

    # Split data
    test_data = lines[:test_size]
    validate_data = lines[test_size:test_size + validate_size]
    train_data = lines[test_size + validate_size:]

    # Write to files
    for data, file in zip([test_data, validate_data, train_data], [test_file, validate_file, train_file]):
        with open(file, 'w') as outfile:
            for line in data:
                outfile.write(line)

# Usage



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Clean and format chat data into JSONL format.")
    parser.add_argument("--input_file", required=True, help="The input text file containing chat data.")
    parser.add_argument("--output_file", default="output_file.jsonl", help="The output JSONL file where the cleaned data will be stored. Default: output_file.jsonl")
    parser.add_argument("--test_file", default="test.jsonl", help="The output JSONL file for test data. Default: test.jsonl")
    parser.add_argument("--valid_file", default="valid.jsonl", help="The output JSONL file for validation data. Default: valid.jsonl")
    parser.add_argument("--train_file", default="train.jsonl", help="The output JSONL file for training data. Default: train.jsonl")

    args = parser.parse_args()

    clean_and_format(args.input_file, args.output_file)
    split_jsonl(args.output_file, args.test_file, args.valid_file, args.train_file)