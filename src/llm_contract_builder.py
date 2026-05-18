from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from src.input_collector import collect_input_corpus
from src.io_utils import write_json
from src.llm_client import LlmConfig, build_llm_client


CONTRACT_SCHEMA_DESCRIPTION = """
Return a single JSON object with this shape:
{
  "domain": "short_domain_name",
  "seed": 20260518,
  "source_inputs": ["relative/path/or/source/name"],
  "entities": {
    "table_name": {
      "primary_key": "column_name"
    }
  },
  "relationships": [
    {
      "from": "child_table.child_column",
      "to": "parent_table.parent_column",
      "cardinality": "many_to_one"
    }
  ],
  "field_generators": {
    "table.column": {
      "type": "faker|id|category|decimal|boolean|date|derived",
      "provider": "optional Faker provider name",
      "description": "brief generation intent"
    }
  },
  "rules": [
    {
      "name": "rule_name",
      "expression": "machine-readable or human-readable rule expression"
    }
  ],
  "validations": [
    {
      "name": "validation_name",
      "required": true
    }
  ]
}
"""


class LlmContractBuilder:
    def __init__(self, config: LlmConfig) -> None:
        self.config = config
        self.client = build_llm_client(config)

    def build(self, input_dir: str | Path, output_contract: str | Path, seed: int = 20260518) -> dict[str, Any]:
        corpus = collect_input_corpus(input_dir)
        prompt = self._build_prompt(corpus, seed)
        response_text = self.client.generate_text(prompt)
        contract = _parse_json_object(response_text)
        contract = _normalize_contract(contract, seed, corpus)
        write_json(output_contract, contract)
        return contract

    def _build_prompt(self, corpus: dict[str, Any], seed: int) -> str:
        return f"""
You are an enterprise synthetic data contract compiler.

Your job:
- Read the user's raw enterprise inputs.
- Infer entities, primary keys, foreign keys, relationships, lifecycle rules, data generators, and validations.
- Create an executable generation contract for a deterministic Python/Faker generator.
- Do not generate synthetic rows.
- Do not include markdown.
- Return valid JSON only.

Important patent architecture:
- LLM performs semantic interpretation.
- Deterministic engine performs scalable data generation.
- Validators prove business and technical correctness.

Seed to use: {seed}

Contract format:
{CONTRACT_SCHEMA_DESCRIPTION}

User input corpus:
{json.dumps(corpus, indent=2)}
""".strip()


def _parse_json_object(text: str) -> dict[str, Any]:
    cleaned = text.strip()
    if cleaned.startswith("```"):
        cleaned = cleaned.strip("`")
        if cleaned.startswith("json"):
            cleaned = cleaned[4:].strip()

    start = cleaned.find("{")
    end = cleaned.rfind("}")
    if start == -1 or end == -1 or end <= start:
        raise ValueError(f"LLM response did not contain a JSON object: {text[:500]}")

    return json.loads(cleaned[start : end + 1])


def _normalize_contract(contract: dict[str, Any], seed: int, corpus: dict[str, Any]) -> dict[str, Any]:
    contract.setdefault("seed", seed)
    contract.setdefault("source_inputs", [file["relative_path"] for file in corpus["files"]])
    contract.setdefault("entities", {})
    contract.setdefault("relationships", [])
    contract.setdefault("field_generators", {})
    contract.setdefault("rules", [])
    contract.setdefault("validations", [])

    required = ["domain", "entities", "relationships", "rules", "validations"]
    missing = [key for key in required if key not in contract]
    if missing:
        raise ValueError(f"Generated contract is missing required keys: {missing}")

    return contract
