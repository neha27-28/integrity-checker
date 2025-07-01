import os
import hashlib

def hash_file(filepath):
    """
    Computes SHA-256 hash of a file.
    Data sent in chunks to avoid file errors and memory leaks.
    """
    sha256 = hashlib.sha256() #creating the object for sha256
    try:
        with open(filepath, 'rb') as f:   # with automatically cakks f.close() when the block ends
            while chunk := f.read(8192):  # Read in chunks upto 8192 bytes (memory-safe) ::: :=->walrus operator
                sha256.update(chunk)
        return sha256.hexdigest()
    except (FileNotFoundError, PermissionError):
        return None  # Could also log this error if needed


def scan_directory(directory):
    """
    Recursively scans all files in a directory and returns a dict of {filepath: hash}
    """
    hash_dict = {}   #creating a dictionary to store the hashes and filepath of the folder
    
    # syntax= root, subdirectories, files
    # uses recursion
    for root, _, files in os.walk(directory):  # _ indicates subdirectories are left out
        for file in files:
            full_path = os.path.join(root, file)

            # Normalize for consistent paths
            normalized_path = os.path.normpath(full_path)
            file_hash = hash_file(normalized_path)
            
            # equivalent to if file_hash is not None
            if file_hash:  # skip unreadable files
                hash_dict[normalized_path] = file_hash

    return hash_dict
