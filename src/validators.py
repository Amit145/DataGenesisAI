from __future__ import annotations

from datetime import date
from typing import Any


def _to_date(value: str) -> date:
    return date.fromisoformat(value)


def validate_dataset(dataset: dict[str, list[dict[str, Any]]], expected_records: int | None = None) -> dict[str, Any]:
    customers = dataset["customers"]
    policies = dataset["policies"]
    claims = dataset["claims"]
    payments = dataset["payments"]

    customer_ids = {row["customer_id"] for row in customers}
    policy_by_id = {row["policy_id"]: row for row in policies}
    claim_by_id = {row["claim_id"]: row for row in claims}

    checks = []

    checks.append(
        {
            "name": "policies_reference_existing_customers",
            "passed": all(row["customer_id"] in customer_ids for row in policies),
        }
    )
    checks.append(
        {
            "name": "claims_reference_existing_policies",
            "passed": all(row["policy_id"] in policy_by_id for row in claims),
        }
    )
    checks.append(
        {
            "name": "payments_reference_existing_claims",
            "passed": all(row["claim_id"] in claim_by_id for row in payments),
        }
    )
    checks.append(
        {
            "name": "claim_date_on_or_after_policy_start",
            "passed": all(
                _to_date(row["claim_date"]) >= _to_date(policy_by_id[row["policy_id"]]["policy_start_date"])
                for row in claims
            ),
        }
    )
    checks.append(
        {
            "name": "payment_date_on_or_after_claim_date",
            "passed": all(
                _to_date(row["payment_date"]) >= _to_date(claim_by_id[row["claim_id"]]["claim_date"])
                for row in payments
            ),
        }
    )
    checks.append(
        {
            "name": "fraud_flag_matches_threshold",
            "passed": all(row["is_fraud_flagged"] == (row["fraud_score"] >= 0.75) for row in claims),
        }
    )
    if expected_records is not None:
        checks.append(
            {
                "name": "requested_volume_is_met",
                "passed": all(len(rows) == expected_records for rows in dataset.values()),
            }
        )

    passed = sum(1 for check in checks if check["passed"])
    return {
        "record_counts": {name: len(rows) for name, rows in dataset.items()},
        "checks": checks,
        "passed_checks": passed,
        "total_checks": len(checks),
        "trust_score": round(passed / len(checks), 4) if checks else 0.0,
        "status": "PASS" if passed == len(checks) else "FAIL",
    }
