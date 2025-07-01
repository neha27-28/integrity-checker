import os
import hashlib

def hash_file(filepath):
    """
    Computes the SHA-256 hash of the specified file.

    Why chunks?
    - Reads file data in chunks (8192 bytes) to handle large files efficiently.
    - Prevents memory overload by not loading the entire file into memory.

    Parameters:
    - filepath (str): Absolute or relative path to the file.

    Returns:
    - str: Hexadecimal digest of the SHA-256 hash.
    - None: If the file cannot be read (due to permission error or if not found).
    """
    sha256 = hashlib.sha256()  # Create a new SHA-256 hash object
    try:
        # Open the file in binary read mode; 'with' handles file closing automatically
        with open(filepath, 'rb') as f:
            # Read the file in chunks using the walrus operator (Python 3.8+)
            while chunk := f.read(8192):
                sha256.update(chunk)  # Update hash with the chunk content
        return sha256.hexdigest()  # Return final hex digest of hash
    except (FileNotFoundError, PermissionError):
        # If the file is not accessible, return None (could be logged instead)
        return None


def scan_directory(directory):
    """
    Recursively scans a directory and computes hashes for all readable files.

    Parameters:
    - directory (str): Root folder to scan.

    Returns:
    - dict: A dictionary where keys are normalized file paths and values are their SHA-256 hashes.
            Format => { "<file_path>": "<sha256_hash>", ... }
    """
    hash_dict = {}  # Initialize dictionary to store {filepath: hash}

    # os.walk() walks through all subdirectories and files recursively
    # We ignore subdirectory names (using _ as convention for unused variable)
    for root, _, files in os.walk(directory):
        for file in files:
            # Construct full file path
            full_path = os.path.join(root, file)

            # Normalize the file path (handles OS-specific formatting)
            normalized_path = os.path.normpath(full_path)

            # Compute file hash
            file_hash = hash_file(normalized_path)

            # If hash is computed successfully, store it in dictionary
            if file_hash:
                hash_dict[normalized_path] = file_hash

    return hash_dict
