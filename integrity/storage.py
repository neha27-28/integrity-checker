import json
import os
from datetime import datetime, timedelta
import shutil
import re


def save_hashes(new_hashes, directory, filepath="data/hashes.json"):
    """
    Saves SHA-256 hash snapshots for a given directory to a central JSON file.

    Functionality:
    - Stores new hash data with a timestamp under the scanned directory's key.
    - Backs up the previous version of the JSON file before saving.
    - Cleans up backups older than 30 days to prevent storage bloat.

    Parameters:
    - new_hashes (dict): Dictionary of {filepath: sha256_hash} from latest scan.
    - directory (str): Top-level directory scanned.
    - filepath (str): Path to the JSON file where hash data is stored (default: "data/hashes.json").
    """

    # Ensure the folder for the JSON file exists
    os.makedirs(os.path.dirname(filepath), exist_ok=True)

    # Step 1: Backup existing JSON before overwriting
    if os.path.exists(filepath):
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        backup_path = f"{filepath}.{timestamp}.bak"
        shutil.copy2(filepath, backup_path)

    # Step 2: Delete backups older than 30 days
    clean_old_backups(filepath)

    # Step 3: Load current hash data from file
    all_data = load_hashes(filepath)

    # Step 4: Add/update hash snapshot under directory key
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if directory not in all_data:
        all_data[directory] = {}

    all_data[directory][timestamp] = new_hashes

    # Step 5: Write updated dictionary back to file
    with open(filepath, "w") as f:
        json.dump(all_data, f, indent=1)


def clean_old_backups(filepath):
    """
    Deletes .bak (backup) files older than 30 days for the given file.

    This helps manage disk space by cleaning outdated snapshots.
    Uses a regex pattern to extract the timestamp embedded in backup filenames.

    Parameters:
    - filepath (str): Original file path whose backups are being managed.
    """
    folder = os.path.dirname(filepath)
    base_name = os.path.basename(filepath)

    for filename in os.listdir(folder):
        # Match pattern: originalfilename.YYYY-MM-DD_HH-MM-SS.bak
        if filename.startswith(base_name) and filename.endswith(".bak"):
            match = re.search(
                r"\.(\d{4}-\d{2}-\d{2}_\d{2}-\d{2}-\d{2})\.bak$", filename
            )
            if match:
                timestamp_str = match.group(1)
                try:
                    backup_time = datetime.strptime(timestamp_str, "%Y-%m-%d_%H-%M-%S")
                    if datetime.now() - backup_time > timedelta(days=30):
                        full_path = os.path.join(folder, filename)
                        os.remove(full_path)
                        print(f"Deleted old backup: {full_path}")
                except ValueError:
                    # Invalid timestamp format, ignore
                    continue


def load_hashes(filepath="data/hashes.json"):
    """
    Loads all stored hash data from the central JSON file.

    Returns:
    - dict: Nested dictionary structure {directory: {timestamp: {filepath: hash}}}
    - Returns empty dict if file doesn't exist or is unreadable/corrupt.
    """
    if not os.path.exists(filepath):
        return {}

    try:
        with open(filepath, "r") as f:
            content = f.read().strip()
            if not content:
                return {}  # Empty file
            return json.loads(content)
    except (json.JSONDecodeError, IOError):
        return {}


def load_hashes_for_directory(directory, filepath="data/hashes.json"):
    """
    Retrieves the most recent snapshot of file hashes for a specific directory.

    Parameters:
    - directory (str): The scanned directory whose hashes are to be loaded.
    - filepath (str): Path to the main JSON hash store.

    Returns:
    - dict: Most recent {filepath: hash} mapping for the given directory.
    - Empty dict if no data found for that directory.
    """
    all_data = load_hashes(filepath)
    snapshots = all_data.get(directory, {})

    if not snapshots:
        return {}

    # Get the latest timestamp snapshot
    latest_timestamp = sorted(snapshots.keys())[-1]
    return snapshots[latest_timestamp]
