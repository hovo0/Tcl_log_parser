import json
import subprocess
import os

def test_log_parser_output():
    # Paths
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    tcl_script = os.path.join(repo_root, 'bin', 'log_parser.tcl')
    logs_path = os.path.join(repo_root, 'example', 'logs')
    generated_json = os.path.join(repo_root, 'test', 'golden', 'parsed_output.json')
    golden_json = os.path.join(repo_root, 'test', 'golden', 'expected_output.json')

    # Run the TCL script
    result = subprocess.run(
        ['tclsh', tcl_script, '-path', logs_path],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    assert result.returncode == 0, f"Tcl script failed: {result.stderr}"

    # Check the output JSON file exists
    assert os.path.exists(generated_json), "Generated JSON output file not found"

    # Load generated and golden JSON data
    with open(generated_json, 'r') as f:
        generated_data = json.load(f)
    with open(golden_json, 'r') as f:
        golden_data = json.load(f)

    # Assert they are equal
    assert generated_data == golden_data, "Parsed JSON does not match golden reference"
