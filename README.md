# Hybrid Enterprise Synthetic Data Generator

Private prototype for an AI-guided deterministic enterprise synthetic data generation framework.

## Core idea

An LLM should not generate millions of rows directly. Instead, it interprets schema, business rules, sample metadata, and user test cases into a machine-readable generation contract. A deterministic Python engine then generates scalable, reproducible synthetic enterprise data and validates it against business expectations.

## Two-phase architecture

### Phase 1: LLM semantic planning

The user adds enterprise inputs under `inputs/<domain>/`:

- `schema.json`
- `business_rules.json`
- `domain_knowledge.md`
- `test_cases.json`

Or, for the easiest workflow, the user can dump raw knowledge under:

```text
inputs/<domain>/raw/
```

Examples of accepted raw files:

- `.ddl` / `.sql` database definitions
- `.md` / `.txt` business rules and domain notes
- `.json` schema, relationship, or model exports
- `.csv` sample rows
- `.yaml` / `.yml` config or rule files

An LLM-facing contract builder reads those files and creates a machine-readable generation contract under `contracts/`.

The current MVP has a deterministic contract-builder stub so the pipeline works without an LLM API key. Later, the same module can call any configured LLM provider using `config/llm_config.local.json`.

### Phase 2: Deterministic generation

The deterministic engine reads the generated contract and creates reproducible synthetic data at scale using Python/Faker/rule logic. Validators then produce a trust/validation report.

## MVP scope

- Domain-flexible architecture
- First demo domain: insurance claims
- Deterministic generation using seed-based execution
- Explicit generation contract
- User/business validation checks
- Validation report for patent evidence and quality proof

## Prototype flow

```text
schema/rules/test cases
  -> generation contract
  -> deterministic generator
  -> synthetic data
  -> validators
  -> validation report
```

## Quick start

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt

python -m src.cli prepare-context --input-dir inputs/insurance_claims --output-context outputs/insurance_claims_llm_context.json
python -m src.cli build-contract --input-dir inputs/insurance_claims --output-contract contracts/insurance_claims_contract.generated.json
python -m src.cli generate --contract contracts/insurance_claims_contract.generated.json --records 1000 --output outputs/demo
```

To build the contract using the configured LLM:

```powershell
python -m src.cli llm-build-contract --input-dir inputs/insurance_claims --output-contract contracts/insurance_claims_contract.llm.generated.json --config config/llm_config.local.json
python -m src.cli generate --contract contracts/insurance_claims_contract.llm.generated.json --records 1000 --output outputs/llm_demo
```

## LLM configuration

Copy `config/llm_config.example.json` to `config/llm_config.local.json` when adding a real LLM provider. Store API keys in environment variables, not in the repo.

PowerShell setup:

```powershell
setx GEMINI_API_KEY "your_api_key_here"
```

Restart PyCharm or the terminal after setting the key. Then test:

```powershell
python -m src.cli test-llm --config config/llm_config.local.json
```

If your IDE or Codex shell cannot see the environment variable, create a local `.env` file:

```text
GEMINI_API_KEY=your_api_key_here
```

`.env` is ignored by Git.

Do not publish this repository publicly before internal IP/legal review.

## Patent working package

The evolving invention notes, architecture, claim ideas, business use cases, and patent evidence plan are in [patent/README.md](patent/README.md). Keep these files private until internal IP/legal review.

