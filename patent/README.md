# Patent Working Package

This folder captures the invention concept, technical novelty, business problem, architecture, claim ideas, and build roadmap for the hybrid enterprise synthetic data generator.

This is not a filed patent application and is not legal advice. It is a technical invention package intended to help prepare an internal invention disclosure for company/legal review.

## Folder contents

- `01_invention_disclosure.md` - main invention disclosure draft.
- `02_novelty_and_differentiation.md` - what makes the idea stronger than generic synthetic data generation.
- `03_system_architecture.md` - technical architecture and flow.
- `04_generation_contract_spec.md` - proposed executable contract concept.
- `05_claim_ideas.md` - informal patent claim ideas for attorney refinement.
- `06_business_use_cases.md` - EXL/global enterprise business problems solved.
- `07_prototype_roadmap.md` - code milestones to prove the invention.
- `08_evidence_log_template.md` - what to record as we build and test.

## Core invention summary

A hybrid AI-guided deterministic enterprise synthetic data generation framework in which a language model interprets schema, domain metadata, business rules, sample patterns, and user test cases into an executable generation contract. A deterministic Python/Faker/rule engine then generates high-volume reproducible synthetic enterprise data, validates the output against business and technical expectations, and optionally repairs the contract using validation feedback.

The key distinction is that the LLM does not generate millions of records directly. The LLM generates the semantic plan. The deterministic engine generates data at scale.
