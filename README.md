# DataGate

[![CI](https://github.com/StratCraftsAI/DataGate/actions/workflows/ci.yml/badge.svg)](https://github.com/StratCraftsAI/DataGate/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)

A deterministic boundary layer for untrusted external data in AI agent systems.

DataGate parses CSV and JSON files through a tool boundary before model analysis. Raw file text never goes straight into model context. Instead, the parser emits structured JSON with field-level metadata and suspicious text annotations, and the model reasons over that structured output.

## Why

When an AI agent ingests external data (CSV exports, API dumps, user-uploaded files), raw text and model instructions share the same channel. This is the [in-band signaling problem](https://en.wikipedia.org/wiki/In-band_signaling): data that says "ignore previous instructions" looks the same as an actual instruction.

DataGate enforces a simple principle: **tool reads data, model processes results**. The parser is deterministic code that does not follow instructions embedded in data. It just parses, annotates, and emits structured output.

## Quick Start

```bash
# Parse a CSV
python3 scripts/ingest_data.py --input data.csv

# Parse a JSON file
python3 scripts/ingest_data.py --input data.json

# Bounded preview for large files
python3 scripts/ingest_data.py --input data.csv --max-preview-rows 10 --max-string-length 120

# Block files larger than 10 MiB
python3 scripts/ingest_data.py --input data.csv --max-input-bytes 10485760
```

Output goes to stdout as JSON. Errors go to stderr with non-zero exit code.

## Output Structure

```json
{
  "source": { "path": "...", "format": "csv", "parser": "...", "limits": {} },
  "summary": { "row_count": 100, "column_count": 5, "preview_rows_truncated": false },
  "schema": { "kind": "table", "fields": [...] },
  "alerts": [{ "kind": "instruction_like_text", "location": {...}, "matched_rules": [...] }],
  "preview_rows": [...]
}
```

See [references/output-schema.md](references/output-schema.md) for the full schema.

## What It Detects

The parser uses conservative string heuristics to flag instruction-like text in data fields:

- "ignore previous instructions" / "disregard prior instructions"
- "system prompt" / "developer prompt"
- "you are now"
- "reveal the system prompt"
- Shell exfiltration patterns (`curl`, `wget`, `printenv`)

These heuristics annotate suspicious text as metadata. They do not filter, block, or classify intent. DataGate is a boundary layer, not a prompt injection detector.

## As a Skill

DataGate ships as a skill for AI coding agents. Install the skill directory and the agent will automatically parse external CSV/JSON through the tool boundary before analyzing it.

See [SKILL.md](SKILL.md) for the full skill definition and workflow.

## Requirements

- Python 3.10+
- No external dependencies (stdlib only)

## License

[MIT](LICENSE)
