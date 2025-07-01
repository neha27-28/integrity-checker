import os
import shutil
from datetime import datetime


def generate_report(changes, scan_dir, output_dir="reports", as_html=False, filename=None):
    os.makedirs(output_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_name = filename or f"report_{timestamp}.{'html' if as_html else 'txt'}"
    report_path = os.path.join(output_dir, report_name)
    
    #backup existing report if it exists
    if os.path.exists(report_path):
        backup_dir=os.path.join(output_dir, "archive")
        os.makedirs(backup_dir, exist_ok=True)
        backup_timestamp=datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name=f"{report_name}.{backup_timestamp}.bak"
        backup_path=os.path.join(backup_dir, backup_name)
        shutil.copy2(report_path, backup_path)
        

    lines = []
    lines.append(f"Scan Report for:{scan_dir}")
    lines.append(f"Scan Time: {datetime.now()}")
    lines.append("")

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

       
    if as_html:
        # simple HTML rendering
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

        html_content += "<body></html>"
        with open(report_path, "w", encoding="utf-8") as f:
            f.write(html_content)

    else:
        with open(report_path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))

    return report_path
