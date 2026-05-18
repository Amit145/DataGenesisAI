from __future__ import annotations

import random
from datetime import timedelta
from typing import Any

from faker import Faker

from src.contracts import GenerationContract


class DeterministicEnterpriseGenerator:
    def __init__(self, contract: GenerationContract) -> None:
        self.contract = contract
        self.fake = Faker("en_US")
        self.fake.seed_instance(contract.seed)
        random.seed(contract.seed)

    def generate_insurance_claims(self, records: int) -> dict[str, list[dict[str, Any]]]:
        customers = []
        policies = []
        claims = []
        payments = []

        for index in range(records):
            customer_id = f"CUST-{index + 1:08d}"
            policy_id = f"POL-{index + 1:08d}"
            claim_id = f"CLM-{index + 1:08d}"

            policy_start = self.fake.date_between(start_date="-5y", end_date="-30d")
            policy_end = policy_start + timedelta(days=random.choice([365, 730, 1095]))
            claim_date = self.fake.date_between(start_date=policy_start, end_date="today")
            claim_amount = round(random.uniform(250.0, 75000.0), 2)
            fraud_score = round(random.betavariate(1.2, 8.0), 4)
            is_fraud_flagged = fraud_score >= 0.75
            payment_date = claim_date + timedelta(days=random.randint(3, 90))
            payment_amount = round(claim_amount * random.uniform(0.65, 1.0), 2)

            customers.append(
                {
                    "customer_id": customer_id,
                    "first_name": self.fake.first_name(),
                    "last_name": self.fake.last_name(),
                    "email": self.fake.unique.email(),
                    "state": self.fake.state_abbr(),
                    "created_date": str(policy_start - timedelta(days=random.randint(1, 365))),
                }
            )
            policies.append(
                {
                    "policy_id": policy_id,
                    "customer_id": customer_id,
                    "policy_type": random.choice(["AUTO", "HOME", "LIFE", "HEALTH"]),
                    "policy_start_date": str(policy_start),
                    "policy_end_date": str(policy_end),
                    "premium_amount": round(random.uniform(500.0, 6000.0), 2),
                    "status": "ACTIVE" if policy_end >= claim_date else "EXPIRED",
                }
            )
            claims.append(
                {
                    "claim_id": claim_id,
                    "policy_id": policy_id,
                    "claim_date": str(claim_date),
                    "claim_amount": claim_amount,
                    "claim_type": random.choice(["ACCIDENT", "THEFT", "WEATHER", "MEDICAL", "PROPERTY"]),
                    "fraud_score": fraud_score,
                    "is_fraud_flagged": is_fraud_flagged,
                    "status": random.choice(["OPEN", "UNDER_REVIEW", "APPROVED", "SETTLED"]),
                }
            )
            payments.append(
                {
                    "payment_id": f"PAY-{index + 1:08d}",
                    "claim_id": claim_id,
                    "payment_date": str(payment_date),
                    "payment_amount": payment_amount,
                    "payment_method": random.choice(["ACH", "CHECK", "WIRE"]),
                }
            )

        return {
            "customers": customers,
            "policies": policies,
            "claims": claims,
            "payments": payments,
        }

    def generate(self, records: int) -> dict[str, list[dict[str, Any]]]:
        if self.contract.domain != "insurance_claims":
            raise ValueError(f"Unsupported MVP domain: {self.contract.domain}")
        return self.generate_insurance_claims(records)
