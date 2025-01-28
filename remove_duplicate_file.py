import os
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend

def calculate_file_hash(file_path):
    """Calculate SHA256 hash of a file using cryptography."""
    digest = hashes.Hash(hashes.SHA256(), backend=default_backend())

    with open(file_path, 'rb') as file:
        for chunk in iter(lambda: file.read(4096), b''):
            digest.update(chunk)

    return digest.finalize().hex()

def remove_duplicates(folder_path):
    file_hashes = {}
    duplicates = []

    for root, _, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)

            file_hash = calculate_file_hash(file_path)

            if file_hash in file_hashes:
                duplicates.append(file_path)
                print(f"Duplicate found: {file_path} (duplicate of {file_hashes[file_hash]})")
            else:
                file_hashes[file_hash] = file_path

    for duplicate in duplicates:
        os.remove(duplicate)
        print(f"Removed: {duplicate}")

    print(f"Removed {len(duplicates)} duplicate file(s).")

def main():
    folder_path = "./std_file"
    remove_duplicates(folder_path)

if __name__ == "__main__":
    main()
