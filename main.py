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
    extension_files = []
    for filename in file_list:
        for ext in entensions:
            extend_files.append(f"{filename}{ext}")
    return extension_files


def find_and_copy_files(file_list, source_folder, found_folder, found_csv):
    not_found_files = set(file_list)
    found_file = []
    std_anl_list = []

    if not os.path.exists(found_folder):
        os.makedirs(found_folder)

    for root, _, files in os.walk(source_folder):
        file_set = set(files)
        matching_files = not_found_files.intersection(file_set)

        std_files = [f for f in files if f.endsewith(".std")]
        anl_files = [f for f in files if f.endsewith(".ANL")]

        for file in files:
            std_status = file if file in std_files else ""
            anl_status = file if file in anl_files else ""
            std_anl_list.append([file, std_status, anl_status])


        matching_files = not_found_files.intersection(file_set)

        for filename in matching_files:
            source_path = os.path.join(root, filename)
            destination_path = os.path.join(found_folder, filename)
            shutil.copy(source_path, destination_path)
            found_file.append((filename, os.path.abspath(destination_path)))

        not_found_files -= matching_files


    with open(found_csv, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Filename", "Path"])  # Correctly write the column headers
        writer.writerows(found_file)          # Write all rows (filename and path)

    with open(std_anl_csv, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Filename", "STD", "ANL"])
        writer.writerows(std_anl_list)

    return list(not_found_files)



def extract_text_from_file(file_path):

    with open(file_path, 'r') as file:
        content = file.read()

    match = re.search(r'\(staad run no\.1\)(.*?)(?=FINISH)', content, re.DOTALL | re.IGNORECASE)

    return match.group(1).strip() if match else None

def process_found_files(found_folder, output_json):
    results = {}  # Correct variable name

    for filename in os.listdir(found_folder):
        file_path = os.path.join(found_folder, filename)
        extracted_text = extract_text_from_file(file_path)
        results[filename] = extracted_text if extracted_text else "No relevant text found"

    with open(output_json, 'w') as json_file:
        json.dump(results, json_file, indent=4)  # Correct variable name



if __name__ == "__main__":
    csv_path = "support_list_tpr.csv"
    source_folder = "./input/Staad"
    found_folder = "./found"
    found_csv = "found_files.csv"
    std_anl_csv = "std_anl_files.csv"  # New CSV for STD and ANL files
    output_json = "output.json"

    if not os.path.exists(csv_path):
        print(f"Support List '{csv_path}' does not exist.")
    else:
        file_list = read_csv_to_list(csv_path)
        # Append both .std and .ANL extensions to file list
        file_list_with_extensions = append_extensions(file_list, [".std", ".ANL"])

        not_found_files = find_and_copy_files(
            file_list_with_extensions, source_folder, found_folder, found_csv, std_anl_csv
        )

        if not_found_files:
            print("The following files were not found:")
            for file in not_found_files:
                print(file)

        process_found_files(found_folder, output_json)
        print(f"Staad Review Completed. Results saved to '{output_json}'.")
        print(f"Found files list saved to '{found_csv}'.")
        print(f"STD and ANL files list saved to '{std_anl_csv}'.")


