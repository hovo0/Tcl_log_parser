# Tcl Log Parser

A Tcl script that recursively scans `.log` files in a given directory and its subdirectories, parses lines starting with `error:`, `warning:`, and `info:`, and outputs a structured JSON summary of the logs.

## Features

- Recursively finds all `.log` files under a specified root directory  
- Parses each log file for lines starting with `error:`, `warning:`, or `info:` (case-insensitive)  
- Stores parsed messages with line numbers in a clean JSON format (without prefixes)  
- Command-line interface to specify the root directory  
- Includes a pytest script to validate output JSON against a golden reference  
- Organized project structure for easy use and testing  

## Installation

Follow these steps to set up the project:

### 1. Clone the Repository
```sh
git clone https://github.com/hovo0/Tcl_log_parser.git
cd Tcl_log_parser
```

### 2. Create a Virtual Environment
```sh
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Requirements
```sh
pip install -r requirements.txt
```


## Usage
Run the Tcl script with the `-path` argument pointing to your logs directory:

```bash
tclsh bin/log_parser.tcl -path ./example/logs
```

This will generate a JSON file at: 
#### test/golden/parsed_output.json 


## Testing
To run the pytest validation:
```bash
pytest test/pytest/test_log_parser.py
```

This test compares the generated JSON with the golden reference to ensure correctness.

