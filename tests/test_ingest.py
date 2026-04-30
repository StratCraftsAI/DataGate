import json
import subprocess
import sys
from pathlib import Path

SCRIPT = Path(__file__).resolve().parent.parent / "scripts" / "ingest_data.py"
FIXTURES = Path(__file__).resolve().parent / "fixtures"


def run_parser(*args):
    result = subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        capture_output=True,
        text=True,
    )
    return result


def test_csv_parse():
    result = run_parser("--input", str(FIXTURES / "sample.csv"))
    assert result.returncode == 0
    output = json.loads(result.stdout)
    assert output["source"]["format"] == "csv"
    assert output["summary"]["row_count"] == 3
    assert output["summary"]["column_count"] == 3
    assert len(output["alerts"]) >= 1
    alert = output["alerts"][0]
    assert alert["kind"] == "instruction_like_text"
    assert alert["location"]["row_index"] == 2


def test_json_parse():
    result = run_parser("--input", str(FIXTURES / "sample.json"))
    assert result.returncode == 0
    output = json.loads(result.stdout)
    assert output["source"]["format"] == "json"
    assert len(output["alerts"]) >= 1


def test_missing_file():
    result = run_parser("--input", "/nonexistent/file.csv")
    assert result.returncode == 1
    assert result.stdout == ""
    error = json.loads(result.stderr)
    assert "error" in error


def test_max_input_bytes():
    result = run_parser("--input", str(FIXTURES / "sample.csv"), "--max-input-bytes", "10")
    assert result.returncode == 1
    error = json.loads(result.stderr)
    assert "too large" in error["error"]
