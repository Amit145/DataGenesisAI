from __future__ import annotations

from pathlib import Path
from typing import Any

from src.io_utils import load_json, read_text, write_json


class InputBundle:
    def __init__(self, input_dir: Path) -> None:
        self.input_dir = input_dir
        self.schema = load_json(input_dir / "schema.json")
        self.business_rules = load_json(input_dir / "business_rules.json")
        self.test_cases = load_json(input_dir / "test_cases.json")
        self.domain_knowledge = read_text(input_dir / "domain_knowledge.md")


class ContractBuilder:
    """Builds generation contracts from user input.

    In the patent architecture, this module is the LLM-facing semantic compiler.
    The current MVP uses deterministic mapping so the pipeline can be tested
    without requiring an LLM API key.
    """

    def build(self, input_dir: str | Path, output_path: str | Path, seed: int = 20260518) -> dict[str, Any]:
        bundle = InputBundle(Path(input_dir))
        contract = self._build_mvp_contract(bundle, seed)
        write_json(output_path, contract)
        return contract

    def _build_mvp_contract(self, bundle: InputBundle, seed: int) -> dict[str, Any]:
        domain = bundle.schema["domain"]
        entities = {}
        relationships = []

        for table in bundle.schema["tables"]:
            primary_keys = [column["name"] for column in table["columns"] if column.get("primary_key")]
            if primary_keys:
                entities[table["name"]] = {"primary_key": primary_keys[0]}

            for column in table["columns"]:
                if "foreign_key" in column:
                    relationships.append(
                        {
                            "from": f"{table['name']}.{column['name']}",
                            "to": column["foreign_key"],
                            "cardinality": "many_to_one",
                        }
                    )

        return {
            "domain": domain,
            "seed": seed,
            "source_inputs": [
                str(bundle.input_dir / "schema.json"),
                str(bundle.input_dir / "business_rules.json"),
                str(bundle.input_dir / "domain_knowledge.md"),
                str(bundle.input_dir / "test_cases.json"),
            ],
            "entities": entities,
            "relationships": relationships,
            "rules": self._map_rules(bundle.business_rules),
            "validations": self._map_validations(bundle.test_cases),
        }

    def _map_rules(self, business_rules: dict[str, Any]) -> list[dict[str, Any]]:
        expressions = {
            "claim_after_policy_start": "claims.claim_date >= policies.policy_start_date",
            "payment_after_claim": "payments.payment_date >= claims.claim_date",
            "fraud_threshold": "claims.is_fraud_flagged == (claims.fraud_score >= 0.75)",
        }
        return [
            {"name": rule["name"], "expression": expressions[rule["name"]]}
            for rule in business_rules["rules"]
            if rule["name"] in expressions
        ]

    def _map_validations(self, test_cases: dict[str, Any]) -> list[dict[str, Any]]:
        return [{"name": test["name"], "required": True} for test in test_cases["test_cases"]]
