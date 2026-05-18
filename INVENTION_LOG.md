# Invention Log

## 2026-05-18

Initial invention direction:

- Pure LLM-based synthetic data generation failed to generate large enterprise-scale datasets because of token/context limits.
- Proposed hybrid approach separates semantic intelligence from scalable execution.
- LLM role: interpret input schema, business rules, metadata, sample records, and user test cases into a structured generation contract.
- Deterministic engine role: generate large-scale synthetic data reproducibly using Python/Faker/rule-based execution.
- Validation role: confirm generated data satisfies user-defined tests, inferred relationships, temporal rules, and referential integrity.

Potential patentable mechanism:

- LLM-generated executable generation contract.
- Deterministic large-volume generation.
- User-supplied test cases embedded into validation.
- Feedback/repair loop that updates the generation contract when validation fails.

Do not disclose publicly before company/legal review.
