# Business Rules

- Every policy must reference an existing customer.
- Every claim must reference an existing policy.
- Every payment must reference an existing claim.
- Claim date must be on or after the policy start date.
- Payment date must be on or after the claim date.
- Fraud flag must be derived from fraud score.
- Fraud flag is true when fraud_score is greater than or equal to 0.75.
- Generated data must be reproducible from the same seed and generation contract.
