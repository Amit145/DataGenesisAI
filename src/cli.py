from __future__ import annotations

import argparse
from pathlib import Path

from src.contract_builder import ContractBuilder
from src.contracts import GenerationContract
from src.generator import DeterministicEnterpriseGenerator
from src.input_collector import write_input_corpus
from src.io_utils import load_json, write_csv, write_json
from src.llm_contract_builder import LlmContractBuilder
from src.llm_client import LlmConfig, build_llm_client
from src.validators import validate_dataset


def test_llm(args: argparse.Namespace) -> None:
    config = LlmConfig.from_file(args.config)
    client = build_llm_client(config)
    response_text = client.test_connection(args.prompt)
    print(f"LLM provider={config.provider} model={config.model}")
    print(f"Response: {response_text}")


def prepare_context(args: argparse.Namespace) -> None:
    corpus = write_input_corpus(args.input_dir, args.output_context)
    print(f"Prepared LLM input corpus from {corpus['file_count']} files")
    print(f"Context written to {args.output_context}")


def build_contract(args: argparse.Namespace) -> None:
    contract = ContractBuilder().build(args.input_dir, args.output_contract, seed=args.seed)
    print(f"Built generation contract for domain={contract['domain']}")
    print(f"Contract written to {args.output_contract}")


def llm_build_contract(args: argparse.Namespace) -> None:
    config = LlmConfig.from_file(args.config)
    contract = LlmContractBuilder(config).build(args.input_dir, args.output_contract, seed=args.seed)
    print(f"Built LLM generation contract for domain={contract['domain']}")
    print(f"Contract written to {args.output_contract}")


def generate_data(args: argparse.Namespace) -> None:
    contract = GenerationContract.from_dict(load_json(args.contract))
    generator = DeterministicEnterpriseGenerator(contract)
    dataset = generator.generate(args.records)
    report = validate_dataset(dataset, expected_records=args.records)

    output_dir = Path(args.output)
    for table_name, rows in dataset.items():
        write_csv(output_dir / f"{table_name}.csv", rows)

    write_json(output_dir / "validation_report.json", report)
    print(f"Generated {args.records} base records into {output_dir}")
    print(f"Validation status: {report['status']} trust_score={report['trust_score']}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Build contracts and generate governed synthetic enterprise data.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    test_llm_parser = subparsers.add_parser("test-llm", help="Test LLM API key and model configuration.")
    test_llm_parser.add_argument("--config", default="config/llm_config.local.json", help="Path to local LLM config.")
    test_llm_parser.add_argument("--prompt", default="Reply with only: API_OK", help="Small test prompt.")
    test_llm_parser.set_defaults(func=test_llm)

    context_parser = subparsers.add_parser("prepare-context", help="Collect raw domain inputs for the LLM phase.")
    context_parser.add_argument("--input-dir", required=True, help="Input folder containing raw or structured files.")
    context_parser.add_argument("--output-context", required=True, help="Path for generated LLM context JSON.")
    context_parser.set_defaults(func=prepare_context)

    build_parser = subparsers.add_parser("build-contract", help="Build a generation contract from input files.")
    build_parser.add_argument("--input-dir", required=True, help="Input folder containing schema/rules/domain/test files.")
    build_parser.add_argument("--output-contract", required=True, help="Path for generated contract JSON.")
    build_parser.add_argument("--seed", type=int, default=20260518, help="Seed to store in the contract.")
    build_parser.set_defaults(func=build_contract)

    llm_build_parser = subparsers.add_parser(
        "llm-build-contract",
        help="Use the configured LLM to build a generation contract from raw input files.",
    )
    llm_build_parser.add_argument("--input-dir", required=True, help="Input folder containing raw or structured files.")
    llm_build_parser.add_argument("--output-contract", required=True, help="Path for generated contract JSON.")
    llm_build_parser.add_argument("--config", default="config/llm_config.local.json", help="Path to local LLM config.")
    llm_build_parser.add_argument("--seed", type=int, default=20260518, help="Seed to store in the contract.")
    llm_build_parser.set_defaults(func=llm_build_contract)

    generate_parser = subparsers.add_parser("generate", help="Generate data from a generation contract.")
    generate_parser.add_argument("--contract", required=True, help="Path to generation contract JSON.")
    generate_parser.add_argument("--records", type=int, default=1000, help="Number of base records to generate.")
    generate_parser.add_argument("--output", default="outputs/demo", help="Output directory.")
    generate_parser.set_defaults(func=generate_data)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
