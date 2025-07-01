import json
import os
from datetime import datetime, timedelta
import shutil
import re


def save_hashes(new_hashes, directory, filepath="data/hashes.json"):
    """
    Saves hashes for a specific directory to a common JSON file.

    Parameters:
    - new_hashes: dict of {filepath: hash} from latest scan
    - directory: the top-level folder scanned
    - filepath: path of the JSON file where all hash data is stored

    Automatically creates a backup of the old file.
    Deletes backups older than 30 days.
    """

    # Ensure that the data directory exists
    os.makedirs(os.path.dirname(filepath), exist_ok=True)

    # backup exisiting file before writing
    if os.path.exists(filepath):
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        backup_path = f"{filepath}.{timestamp}.bak"
        shutil.copy2(filepath, backup_path)

    # delete backups older than 30 days
    clean_old_backups(filepath)

    # load existing hash Data
    all_data = load_hashes(filepath)

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if directory not in all_data:
        all_data[directory] = {}

    # save updated data back to JSON
    all_data[directory][timestamp] = new_hashes

    with open(filepath, "w") as f:
        json.dump(all_data, f, indent=1)


def clean_old_backups(filepath):
    """
    Deletes .bak files older than 30m days in the same directory as the filepath.
    """
    folder = os.path.dirname(filepath)
    base_name = os.path.basename(filepath)

    for filename in os.listdir(folder):
        if filename.startswith(base_name) and filename.endswith(".bak"):
            # extract timestamp from filename using the regex
            match = re.search(
                r"\.(\d{4}-\d{2}-\d{2}_\d{2}-\d{2}-\d{2})\.bak$", filename)
            if match:
                timestamp_str = match.group(1)
                try:
                    backup_time = datetime.strptime(
                        timestamp_str, "%Y-%m-%d_%H-%M-%S")
                    if datetime.now()-backup_time > timedelta(days=30):
                        full_path = os.path.join(folder, filename)
                        os.remove(full_path)
                        print(f"Deleted old backups: {full_path}")
                except ValueError:
                    continue


def load_hashes(filepath="data/hashes.json"):
    """
    Loads the hash dictionary from a JSON file.
    Returns an empty dict if file doesn't exist or is empty/invalid.
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
    # loads stored hashes for a specific directory from the JSON file.

    all_data = load_hashes(filepath)
    snapshots = all_data.get(directory, {})

    if not snapshots:
        return {}

    # get the latest snapshot by timestamp
    latest_timestamp = sorted(snapshots.keys())[-1]
    return snapshots[latest_timestamp]
