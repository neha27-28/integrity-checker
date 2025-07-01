import os
import shutil
from datetime import datetime

def generate_report(changes, scan_dir, output_dir="reports", as_html=False, filename=None):
    """
    Generates a report summarizing file integrity changes (new, modified, deleted) for a given directory.

    Parameters:
    - changes (dict): Dictionary with keys 'new', 'modified', 'deleted' and lists of corresponding files.
    - scan_dir (str): The directory path that was scanned.
    - output_dir (str): Directory where the report will be saved. Defaults to 'reports'.
    - as_html (bool): Whether to generate the report in HTML format. Defaults to False (plain text).
    - filename (str): Optional custom filename for the report. If not provided, a timestamped name is generated.

    Returns:
    - str: Full path to the generated report file.
    """

    # Ensure the reports directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Generate a default filename if not provided
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_name = filename or f"report_{timestamp}.{'html' if as_html else 'txt'}"
    report_path = os.path.join(output_dir, report_name)

    # STEP 1: Backup any existing report with the same name
    if os.path.exists(report_path):
        backup_dir = os.path.join(output_dir, "archive")
        os.makedirs(backup_dir, exist_ok=True)

        backup_timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"{report_name}.{backup_timestamp}.bak"
        backup_path = os.path.join(backup_dir, backup_name)

        # Make a copy of the old report before overwriting
        shutil.copy2(report_path, backup_path)

    # STEP 2: Construct report content as a list of lines (for plain text)
    lines = []
    lines.append(f"Scan Report for: {scan_dir}")
    lines.append(f"Scan Time: {datetime.now()}")
    lines.append("")

    # Check if there are any changes to report
    has_changes = any(changes.values())

    if not has_changes:
        lines.append("No changes detected.")
    else:
        for section in ["new", "modified", "deleted"]:
            if changes.get(section):
                lines.append(f"{section.capitalize()} Files:")
                for file in changes[section]:
                    lines.append(f"    - {file}")
                lines.append("")

    # STEP 3: Output the report to HTML or plain text
    if as_html:
        # Basic HTML formatting
        html_content = f"""
        <html>
        <head><title>File Integrity Report</title></head>
        <body>
            <h2>Scan Report for: {scan_dir}</h2>
            <p><strong>Scan Time:</strong> {datetime.now()}</p>
        """

        if not has_changes:
            html_content += "<p>No changes detected.</p>"
        else:
            for key in ["new", "modified", "deleted"]:
                if changes.get(key):
                    html_content += f"<h3>{key.capitalize()} Files:</h3><ul>"
                    for file in changes[key]:
                        html_content += f"<li>{file}</li>"
                    html_content += "</ul>"

        html_content += "</body></html>"

        # Write HTML content to file
        with open(report_path, "w", encoding="utf-8") as f:
            f.write(html_content)

    else:
        # Write plain text content to file
        with open(report_path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))

    return report_path
