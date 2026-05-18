# System Architecture

## High-level architecture

```text
User Inputs
  - DDL / SQL
  - schema
  - ER model / relationship notes
  - domain description
  - business rules
  - sample patterns
  - desired volume
  - user test cases
        |
        v
LLM Semantic Interpreter
  - identifies entities and fields
  - infers relationships
  - maps business rules
  - converts test cases into validation expectations
  - proposes distributions and generators
        |
        v
Executable Generation Contract
  - entities and fields
  - generator mappings
  - relationships and cardinality
  - temporal lifecycle rules
  - distributions
  - validation expectations
  - seed and reproducibility configuration
        |
        v
Deterministic Generation Engine
  - Python/Faker providers
  - rule execution
  - relationship graph generation
  - temporal event generation
  - scalable batch generation
        |
        v
Validation Engine
  - referential integrity
  - business rules
  - temporal rules
  - user test cases
  - distribution checks
  - privacy/governance checks
        |
        v
Feedback and Repair Loop
  - failed checks summarized
  - contract revised
  - regeneration or targeted repair
        |
        v
Synthetic Enterprise Data Package
  - data files/tables
  - generation contract
  - validation report
  - trust score
  - lineage/reproducibility metadata
```

## Key modules planned in code

- `input_collector`: collects arbitrary raw enterprise input files into an LLM-readable corpus.
- `contract_builder`: turns schema/rules/test cases into a generation contract. Initially manual, later LLM-assisted.
- `contracts`: typed representation of the generation contract.
- `generator`: deterministic execution engine.
- `validators`: rule and test validation.
- `repair_loop`: validation feedback to contract revision.
- `reports`: evidence, lineage, trust score, and summary reports.
- `providers`: domain-specific generator providers.

## MVP implementation strategy

The first implementation supports a two-phase flow. A deterministic contract-builder stub reads raw input files from `inputs/insurance_claims` and emits a generation contract. This proves the folder structure, contract handoff, deterministic generator, validation engine, and report flow before adding real LLM-based contract generation. After that, the LLM layer can be added without changing the deterministic core.
