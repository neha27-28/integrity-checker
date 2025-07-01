from integrity.scanner import scan_directory
from integrity.storage import save_hashes, load_hashes_for_directory
from integrity.logging_config import setup_logger
from integrity.report import generate_report
from datetime import datetime

import sys

if __name__ == "__main__":
    folder = sys.argv[1] if len(sys.argv) > 1 else input(
        "Enter the folder path to scan: ").strip()
    current = scan_directory(folder)

    print("Current hashes:")
    for p, h in current.items():
        print(f"{p}-> {h}")

    old = load_hashes_for_directory(folder)
    print(f"previously stored: {len(old)} files fo this folder")

    logger = setup_logger()
    logger.info(f"File Integrity Checker started for the folder:{folder}")

    # comparing old and new hashes
    changes = {
        "new": [],
        "modified": [],
        "deleted": []
    }

    # detect new and modified files
    for file, hash in current.items():
        if file not in old:
            changes["new"].append(file)
        elif old[file] != hash:
            changes["modified"].append(file)

    # detect deleted files
    for file in old:
        if file not in current:
            changes["deleted"].append(file)

    # log change counts
    logger.info(
        f"New:{len(changes['new'])}, Modified:{len(changes['modified'])}, Deleted:{len(changes['deleted'])}")

    print("\nSummary of changes:")
    for cat, files in changes.items():
        print(f"{cat.capitalize()}:{len(files)} file(s)")

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = generate_report(
        changes, folder, as_html=True, filename=f"report_{timestamp}.html")
    print(f"Report saved to : {report_path}")

    save_hashes(current, folder)  # save to JSON
    print("\n Hashes saved and preserved.")
