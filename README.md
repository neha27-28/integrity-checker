# File Integrity Checker CLI Tool

A command-line interface (CLI) tool that helps ensure the integrity of critical files by computing and comparing SHA-256 checksums. It maintains a record of file states in JSON format and generates detailed reports highlighting any changes such as newly added, modified, or deleted files.

---

## Features

- SHA-256 hash calculation and comparison for selected files.
- Stores all hash data and file metadata in structured JSON format.
- Automatically generates HTML reports showing:
  - Newly added files
  - Modified files
  - Deleted files
  - A "No changes detected" message when applicable.
- Logging of all significant events and operations.
- Automatic cleanup and backup of stored hashes older than 30 days.

---

## Project Structure



file\_integrity\_checker/
├── integrity/              # Core logic and modules for hash computation and comparison
├── venv/                   # Virtual environment (excluded from version control)
├── main.py                 # Entry point to run the CLI tool
├── run\_integrity.bat       # Windows batch script to execute the checker
├── requirements.txt        # Python dependencies
├── README.md               # Project documentation
├── .gitignore              # Git ignore file



> Note: The `logs/`, `data/`, and `reports/` directories are excluded from version control for privacy and security purposes.

---

## Installation

1. Clone the repository:


git clone https://github.com/your-username/file_integrity_checker.git
cd file_integrity_checker


2. (Optional but recommended) Create a virtual environment:


python -m venv venv

3. Activate the virtual environment:

* On Windows:

  ```
  venv\Scripts\activate
  ```

* On macOS/Linux:

  ```bash
  source venv/bin/activate
  ```

4. Install the required packages:

```bash
pip install -r requirements.txt
```

---

## Usage

Run the integrity checker using the main Python script or the batch file:

```bash
python main.py
```

Or on Windows:

```bash
run_integrity.bat
```

The tool will:

* Compute or update file hashes
* Compare them with stored values
* Generate a new report in HTML format
* Log all activity for traceability

---

## Configuration and Extensibility

* All core logic resides in the `integrity/` folder, allowing for modular development and testing.
* Reports are generated in HTML format and can be customized as per user requirements.
* The cleanup mechanism for old hash backups can be configured as needed.

---

## Contributing

Contributions, bug reports, and feature suggestions are welcome. Please fork the repository and submit a pull request with a clear explanation of your changes.

---

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

---

## Author

**Neha Kasera**
B.Tech Student | Cybersecurity Enthusiast | Developer

```

---

You can copy the entire content above into a file named `README.md`. Let me know if you'd also like a `LICENSE`, `.gitignore`, or `requirements.txt` template to complete the repository.
```
