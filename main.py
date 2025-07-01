# Importing core modules from the integrity package
from integrity.scanner import scan_directory  # Scans the target directory and computes SHA-256 hashes for files
from integrity.storage import save_hashes, load_hashes_for_directory  # Handles saving/loading hash data in JSON format
from integrity.logging_config import setup_logger  # Configures and returns a logger instance
from integrity.report import generate_report  # Generates an HTML report based on detected changes
from datetime import datetime  # For timestamping the report and backups

import sys  # To handle command-line arguments

if __name__ == "__main__":
    # STEP 1: Get the folder path from the user (via CLI argument or input prompt)
    folder = sys.argv[1] if len(sys.argv) > 1 else input("Enter the folder path to scan: ").strip()

    # STEP 2: Scan the current state of the folder and generate SHA-256 hashes for each file
    current = scan_directory(folder)

    print("Current hashes:")
    for p, h in current.items():
        print(f"{p} -> {h}")

    # STEP 3: Load the previously saved hashes for this folder from JSON (if available)
    old = load_hashes_for_directory(folder)
    print(f"Previously stored: {len(old)} file(s) for this folder")

    # STEP 4: Set up logging
    logger = setup_logger()
    logger.info(f"File Integrity Checker started for the folder: {folder}")

    # STEP 5: Initialize change tracking dictionary
    changes = {
        "new": [],       # Files that are newly added
        "modified": [],  # Files that existed but have changed content (different hash)
        "deleted": []    # Files that were present earlier but are now missing
    }

    # STEP 6: Compare current file hashes with previous hashes
    for file, hash in current.items():
        if file not in old:
            changes["new"].append(file)  # New file
        elif old[file] != hash:
            changes["modified"].append(file)  # File modified

    # STEP 7: Detect files that were deleted (i.e., present in old but missing in current)
    for file in old:
        if file not in current:
            changes["deleted"].append(file)

    # STEP 8: Log the summary of detected changes
    logger.info(
        f"New: {len(changes['new'])}, Modified: {len(changes['modified'])}, Deleted: {len(changes['deleted'])}"
    )

    # STEP 9: Print a summary of changes to the user
    print("\nSummary of changes:")
    for category, files in changes.items():
        print(f"{category.capitalize()}: {len(files)} file(s)")

    # STEP 10: Generate an HTML report based on the changes
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = generate_report(
        changes,
        folder,
        as_html=True,
        filename=f"report_{timestamp}.html"
    )
    print(f"Report saved to: {report_path}")

    # STEP 11: Save the current hashes back to storage (JSON file)
    save_hashes(current, folder)
    print("\nHashes saved and preserved.")
