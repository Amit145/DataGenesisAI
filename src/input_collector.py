from __future__ import annotations

import csv
from pathlib import Path
from typing import Any

from src.io_utils import read_text, write_json


SUPPORTED_TEXT_SUFFIXES = {
    ".csv",
    ".ddl",
    ".json",
    ".md",
    ".sql",
    ".txt",
    ".yaml",
    ".yml",
}


def collect_input_corpus(input_dir: str | Path) -> dict[str, Any]:
    """Collect arbitrary user-provided domain input files for the LLM phase."""

    root = Path(input_dir)
    raw_dir = root / "raw"
    scan_root = raw_dir if raw_dir.exists() else root

    files = []
    for path in sorted(scan_root.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in SUPPORTED_TEXT_SUFFIXES:
            continue

        text = read_text(path)
        file_payload: dict[str, Any] = {
            "path": str(path),
            "relative_path": str(path.relative_to(root)),
            "suffix": path.suffix.lower(),
            "content": text,
        }

        if path.suffix.lower() == ".csv":
            file_payload["csv_preview"] = _preview_csv(path)

        files.append(file_payload)

    return {
        "input_dir": str(root),
        "scan_root": str(scan_root),
        "file_count": len(files),
        "files": files,
        "llm_instruction": (
            "Read these enterprise input files and create an executable generation contract. "
            "Infer entities, fields, relationships, field generators, business rules, temporal rules, "
            "validations, distributions, and reproducibility settings. The deterministic generator will "
            "execute the contract; do not generate raw records directly."
        ),
    }


def write_input_corpus(input_dir: str | Path, output_path: str | Path) -> dict[str, Any]:
    corpus = collect_input_corpus(input_dir)
    write_json(output_path, corpus)
    return corpus


def _preview_csv(path: Path, max_rows: int = 5) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        return [row for _, row in zip(range(max_rows), reader)]
