# Contributing to DataGate

## Current Policy

**Pull requests are limited to bug fixes and heuristic improvements.** Feature PRs will not be accepted at this time.

Issues and discussions are welcome for bug reports, false positive/negative reports on heuristics, and feature ideas.

## Bug Fix PRs

To submit a bug fix:

1. Open an issue describing the bug with reproduction steps
2. Fork the repository and create a branch from `main`
3. Fix the bug and add a test case that reproduces it
4. Ensure all existing tests pass
5. Submit a PR referencing the issue

## Running Locally

### Requirements

- Python 3.10+
- No external dependencies (stdlib only)

### Usage

```bash
git clone https://github.com/StratCraftsAI/DataGate.git
cd DataGate

# Parse a CSV file
python3 scripts/ingest_data.py --input /path/to/file.csv

# Parse a JSON file
python3 scripts/ingest_data.py --input /path/to/file.json

# Run tests
python3 -m pytest tests/
```

## Code Standards

- Python 3.10+ compatible
- No external dependencies (stdlib only)
- All output goes to stdout as JSON; errors go to stderr
- Non-zero exit code on failure

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
