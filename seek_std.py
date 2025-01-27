import os
import shutil
import csv

def find_std_files(source_folder, destination_folder, csv_path):

    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    std_files = []

    for root, _, files in os.walk(source_folder):
        for file in files:
            if file.endswith(".std"):
                file_path = os.path.join(root, file)
                std_files.append((file, file_path))

                # Copy the file to the destination folder
                shutil.copy(file_path, os.path.join(destination_folder, file))

    # Write the file details to a CSV
    with open(csv_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["File Name", "File Location"])
        writer.writerows(std_files)

    print(f"{len(std_files)} .std files found and copied to '{destination_folder}'.")
    print(f"File details saved to '{csv_path}'.")

if __name__ == "__main__":
    source_folder = "./input"  # Replace with your source folder path
    destination_folder = "./std_file"
    csv_path = "std_files_list.csv"

    find_std_files(source_folder, destination_folder, csv_path)
