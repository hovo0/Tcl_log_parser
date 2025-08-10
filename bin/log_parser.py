"""This is the same script as the Tcl script but written in Python.
The program's main processing is done in Tcl,
this is just a Python representation."""


import os
import sys
import json

if len(sys.argv) != 3 or sys.argv[1] != "-path":
    print(f"Usage: {sys.argv[0]} -path <logs_root_path>")
    sys.exit(1)

root_path = sys.argv[2]

def find_log_files(directory):
    '''Recursively search for all .log files in the given directory.
    Arguments:
        dir - directory to search in
    Returns:
        list of full paths to .log files'''
    log_files = []
    for dirpath, _, filenames in os.walk(directory):
        for filename in filenames:
            if filename.lower().endswith(".log"):
                log_files.append(os.path.join(dirpath, filename))
    return log_files

result = {}
for file_path in find_log_files(root_path):
    file_data = {"Error": {}, "Warning": {}, "Info": {}}
    with open(file_path, "r", errors="ignore") as f:
        for i, line in enumerate(f, start=1):
            lower_line = line.strip().lower()
            if lower_line.startswith("error:"):
                file_data["Error"][str(i)] = line.strip()
            elif lower_line.startswith("warning:"):
                file_data["Warning"][str(i)] = line.strip()
            elif lower_line.startswith("info:"):
                file_data["Info"][str(i)] = line.strip()
    result[os.path.basename(file_path)] = file_data

script_dir = os.path.dirname(os.path.abspath(__file__))
out_dir = os.path.join(script_dir, "..", "test", "golden")
os.makedirs(out_dir, exist_ok=True)
out_file = os.path.join(out_dir, "parsed_output.json")

with open(out_file, "w", encoding="utf-8") as f:
    json.dump(result, f, indent=2, ensure_ascii=False)

print(f"JSON saved to {out_file}")
