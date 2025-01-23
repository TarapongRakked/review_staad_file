import re
import os
import csv
import json
import shutil
from collections import defaultdict

def read_csv_to_list(csv_path):

    with open(csv_path, 'r') as file:
        reader = csv.reader(file)
        return [row[0] for row in reader if row]


def append_extension(file_list, extension):
    return [f"{filename}{extension}" for filename in file_list]


def find_and_copy_files(file_list, source_folder, found_folder, found_csv):

    not_found_files = set(file_list)
    found_file = []

    if not os.path.exists(found_folder):
        os.makedirs(found_folder)

    for root, _, files in os.walk(source_folder):
        file_set = set(files)
        matching_files = not_found_files.intersection(file_set)

        for filename in matching_files:
            source_path = os.path.join(root, filename)
            destination_path = os.path.join(found_folder, filename)
            shutil.copy(source_path, destination_path)
            found_file.append(filename, os.path.abspath(found_folder))

        not_found_files -= matching_files

    with open(found_csv, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(csvfile)
            writer.writerows(found_file)

    return list(not_found_files)


def extract_text_from_file(file_path):

    with open(file_path, 'r') as file:
        content = file.read()

    match = re.search(r'\(staad run no\.1)(.*?)(?=FINISH)', content, re.DOTALL | re.IGNORECASE)
    return match.group(1).strip() if match else None

def process_found_files(found_folder, output_json):

    results = {}

    for filename in os.listdir(found_folder):
        file_path = os.path.join(found_folder, filename)
        extracted_text = extract_text_from_file(file_path)
        results[filename] = extracted_text if extracted_text else "No relevant text found"

    with open(output_json, 'w') as json_file:
        json.dump(result, json_file, indent = 4)

if __name__ == "__main__":
    csv_path = "ps_list.csv"
    source_folder = "./input/staad"
    found_folder = "./found"
    found_csv = "found_files.csv"
    output_json = "output.json"

    if not os.path.exists(csv_path):
        print(f"Support List '{csv_path}' does not exist.")

    else:
        file_list = read_csv_to_list(csv_path)
        file_list_with_extension = append_extension(file_list, ".std")

        not_found_files = find_and_copy_files(file_list_with_extension, source_folder, found_folder, found_csv)

        if not_found_files:
            print("The followint files were not found:")
            for file in not_found_files:
                print(file)

        process_found_files(found_folder, output_json)
        print(f"Staad Review Completed.Results saved to '{output_json}")
        print(f"Found files list saved to '{found_csv}'.")

    


