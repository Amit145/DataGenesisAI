# Generation Contract Specification

## Purpose

The generation contract is the central patent-worthy artifact. It is a machine-readable plan that bridges AI semantic interpretation and deterministic scalable generation.

The LLM should output or revise this contract. The deterministic engine should execute it.

## Contract sections

```json
{
  "domain": "insurance_claims",
  "seed": 20260518,
  "entities": {},
  "relationships": [],
  "field_generators": {},
  "business_rules": [],
  "temporal_rules": [],
  "distributions": [],
  "validations": [],
  "output": {},
  "lineage": {}
}
```

## Required concepts

### Entities

Tables, files, or event types to generate.

Examples:

- customers
- policies
- claims
- payments

### Relationships

Foreign-key and graph dependencies.

Examples:

- policies.customer_id -> customers.customer_id
- claims.policy_id -> policies.policy_id
- payments.claim_id -> claims.claim_id

### Field generators

Mapping of each field to a deterministic generator.

Examples:

- email -> faker.email
- claim_amount -> random_float with range and distribution
- fraud_score -> beta distribution
- status -> weighted category list

### Business rules

Rules that must hold in the generated data.

Examples:

- claim_date >= policy_start_date
- payment_date >= claim_date
- is_fraud_flagged == fraud_score >= threshold

### Temporal rules

Lifecycle/event order rules.

Examples:

- customer created before policy created
- policy exists before claim
- claim exists before payment

### Validations

User-supplied or inferred tests that are run after generation.

Examples:

- all foreign keys must resolve
- no payment before claim
- minimum fraud-flag rate is within expected range
- record counts match requested volume

### Reproducibility

The contract includes seed and version metadata so the same contract can reproduce the same dataset.

## Patent relevance

The generation contract is stronger than raw prompting because it is executable, auditable, testable, and scalable. It allows the LLM to perform semantic planning while deterministic code performs controlled generation.
