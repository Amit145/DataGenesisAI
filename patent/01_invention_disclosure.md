# Invention Disclosure Draft v0.1

## Working title

Hybrid AI-Guided Deterministic Enterprise Synthetic Data Generation System with Executable Business Simulation Contracts and Validation Feedback

## Short title

AI-Guided Deterministic Enterprise Synthetic Data Generator

## Inventive concept

The invention separates semantic interpretation from scalable data generation. A language model interprets enterprise schema, domain metadata, business rules, sample records, and user-provided test cases. Instead of generating raw rows, the language model creates a machine-readable generation contract. A deterministic generation engine executes the contract to create large synthetic datasets with referential integrity, temporal consistency, reproducibility, and validation evidence.

## Problem observed

A pure LLM-based synthetic data approach failed to generate approximately one million enterprise records because the model ran into token/context limitations. Even when smaller datasets can be generated, pure LLM output may become inconsistent, difficult to reproduce, expensive to scale, and unreliable for enterprise relationships and business rules.

## Business problem

Enterprises need realistic synthetic data for testing, analytics, model development, migration, demos, and training. However, regulated organizations often cannot use production data freely because of privacy, compliance, security, client confidentiality, and access restrictions. Existing synthetic data tools may create random or statistically plausible records but often fail to preserve enterprise semantics, cross-table relationships, lifecycle behavior, user-defined test expectations, and audit evidence.

## Proposed solution

The proposed system receives user input such as schema, metadata, business rules, domain description, sample data, desired volume, and test cases. A language model converts these inputs into an executable generation contract. A deterministic engine then generates the requested volume of records using reproducible seeds, Faker-style providers, rule execution, relationship generation, and temporal lifecycle logic. A validation engine checks the generated output against explicit test cases, inferred constraints, referential integrity, temporal rules, distribution expectations, and privacy/governance checks. Failed validations can be fed back to revise the generation contract before regeneration.

## Core technical flow

1. Receive enterprise schema, domain details, rules, sample patterns, and user test cases.
2. Use an LLM as a semantic interpreter and planning layer.
3. Produce a structured generation contract rather than raw records.
4. Execute the contract using deterministic Python/Faker/rule-based generation.
5. Generate high-volume synthetic data across related tables or event streams.
6. Validate output using business rules, referential integrity, temporal checks, and user test cases.
7. Produce validation, trust, lineage, and reproducibility reports.
8. Optionally revise the generation contract using validation failures and regenerate or repair data.

## Why this is different

The invention is not simply using AI to create fake data. The LLM acts as a semantic compiler from business intent into deterministic generation instructions. The deterministic engine handles scale and reproducibility. The validation layer proves whether generated data satisfies business expectations. This hybrid separation directly addresses token limitations, cost, consistency, and auditability.

## Example MVP domain

Insurance claims:

- Customers
- Policies
- Claims
- Payments

Example rules:

- Every policy references a valid customer.
- Every claim references a valid policy.
- Claim date must be on or after policy start date.
- Payment date must be on or after claim date.
- Fraud flag must match a configurable fraud-score threshold.
- Generated records must satisfy user-supplied validation tests.

## Intended outputs

- Synthetic data files or database tables.
- Generation contract used for execution.
- Validation report.
- Lineage and reproducibility metadata.
- Trust score or quality score.
- Failed-test feedback for contract repair.

## Potential assignee/inventor note

If this is submitted through a company IP process, the human contributors should be listed as inventors according to legal review, and the company may become assignee depending on employment/IP policies. Do not publicly publish the code or documentation before internal review.
