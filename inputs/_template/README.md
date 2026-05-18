# Domain Input Template

Create a new folder under `inputs/` for each domain or client use case.

The simplest user experience is:

```text
inputs/<domain_name>/raw/
```

Then dump anything useful into `raw/`:

- DDL files
- ER model notes
- table/column descriptions
- business rules
- domain knowledge
- sample rows
- test cases
- data quality expectations
- relationship notes

The LLM phase will read this input corpus and convert it into an executable generation contract for the deterministic generator.

Recommended optional structure:

```text
inputs/<domain_name>/
  raw/
    schema.ddl
    relationships.md
    business_rules.md
    sample_rows.csv
    test_cases.md
  schema.json
  business_rules.json
  domain_knowledge.md
  test_cases.json
```

The structured files are optional long term. The goal is to support raw enterprise knowledge dumps first.
