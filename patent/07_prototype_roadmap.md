# Prototype Roadmap

## Phase 1 - Deterministic MVP

Status: started.

Goals:

- Manual generation contract.
- Insurance claims demo domain.
- Deterministic Faker-based generator.
- CSV output.
- Validation report with trust score.

Success evidence:

- Generate 1,000 records.
- Generate 100,000 records.
- Generate 1,000,000 records.
- Same seed and same contract reproduce identical output.
- All validations pass.

## Phase 2 - Generic contract execution

Goals:

- Move hardcoded insurance logic into configurable provider mappings.
- Support multiple entity definitions from contract.
- Support common generators, distributions, categorical weights, and date dependencies.

## Phase 3 - User test case engine

Goals:

- Accept user test cases in JSON/YAML.
- Run tests against generated data.
- Include test results in validation report.

## Phase 4 - LLM contract builder

Goals:

- Input: schema, rules, sample rows, domain description, test cases.
- Output: generation contract.
- Human review mode before execution.

## Phase 5 - Feedback/repair loop

Goals:

- Convert failed validations into contract repair instructions.
- Regenerate or patch failed portions.
- Compare before/after trust score.

## Phase 6 - Enterprise package

Goals:

- Lineage report.
- Privacy-risk checks.
- Bias/distribution drift checks.
- CLI and simple API.
- Domain templates for insurance, banking, healthcare, and retail.

## Patent evidence milestones

- Capture token-limit problem statement.
- Capture architecture diagram.
- Capture generation contract examples.
- Capture 1M-record generation result.
- Capture validation report.
- Capture reproducibility proof.
- Capture feedback/repair example.
