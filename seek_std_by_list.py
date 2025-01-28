import os
import csv

def read_names_from_csv(file_path):
    """
    Read a list of names from the first column of a CSV file.

    Args:
        file_path (str): Path to the CSV file.

    Returns:
        list: A list of names from the CSV file.
    """
    with open(file_path, mode='r', newline='', encoding="utf-8") as file:
        reader = csv.reader(file)
        names = [row[0].strip() for row in reader if row]

    return names

def search_files(base_dir, names):
    """
    Search for files in a directory and subdirectories that match the given names.

    Args:
        base_dir (str): The base directory to search in.
        names (list): List of names to search for in file names.

    Returns:
        tuple: A list of found files and a set of names not found.
    """
    found_files = []
    not_found_names = set(names)

    for root, _, files in os.walk(base_dir):
        for file in files:
            for name in names:
                if name in file:
                    found_files.append((name, os.path.join(root, file)))
                    not_found_names.discard(name)
    
    return found_files, not_found_names

def write_csv(file_path, rows, headers=None):
    """
    Write rows to a CSV file with optional headers.

    Args:
        file_path (str): Path to the output CSV file.
        rows (list): Rows of data to write.
        headers (list, optional): Optional list of column headers.
    """
    with open(file_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        if headers:
            writer.writerow(headers)
        writer.writerows(rows)

def main():
    """
    Main function to execute the search and write results to CSV files.
    """
    input_csv = "support_list_tpr.csv"
    search_folder = "./input/Staad"
    output_found_csv = "file_found_seek_by_list.csv"
    output_not_found_csv = "file_not_found_seek_by_list.csv"

    names = read_names_from_csv(input_csv)

    found_files, not_found_names = search_files(search_folder, names)

    write_csv(output_found_csv, found_files, headers=["name", "file_path"])
    write_csv(output_not_found_csv, [(name,) for name in not_found_names], headers=["name"])

    print(f"Search complete, results saved to '{output_found_csv}' and '{output_not_found_csv}'.")

if __name__ == "__main__":
    main()