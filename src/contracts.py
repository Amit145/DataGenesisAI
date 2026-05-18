from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class GenerationContract:
    """Executable plan produced by an AI or human-authored contract."""

    domain: str
    seed: int
    entities: dict[str, Any]
    relationships: list[dict[str, Any]]
    rules: list[dict[str, Any]]
    validations: list[dict[str, Any]]
    source_inputs: list[str]

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "GenerationContract":
        return cls(
            domain=payload["domain"],
            seed=int(payload.get("seed", 42)),
            entities=payload.get("entities", {}),
            relationships=payload.get("relationships", []),
            rules=payload.get("rules", []),
            validations=payload.get("validations", []),
            source_inputs=payload.get("source_inputs", []),
        )
