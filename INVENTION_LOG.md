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

## 2026-05-18 - First LLM-to-deterministic generation loop

Milestone:

- Added Gemini API support through a provider-configurable LLM client.
- Added `llm-build-contract` command.
- Gemini read raw insurance input files from `inputs/insurance_claims/raw`.
- Gemini generated `contracts/insurance_claims_contract.llm.generated.json`.
- The generated contract included inferred entities, relationships, field generators, business rules, and validations.
- Deterministic generator executed the LLM-generated contract for 100 base records.
- Validation passed with `trust_score=1.0`.

Patent relevance:

- Demonstrates the core hybrid mechanism: LLM performs semantic compilation from raw enterprise knowledge into a generation contract, while deterministic code performs scalable data creation and validation.
- Confirms the LLM is not generating synthetic rows directly.
- Provides early evidence for the contract-based handoff and validation-backed trust loop.
