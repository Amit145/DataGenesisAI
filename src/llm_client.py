from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from dataclasses import dataclass
from typing import Any

from src.io_utils import load_json


@dataclass(frozen=True)
class LlmConfig:
    provider: str
    model: str
    api_key_env: str
    temperature: float
    max_output_tokens: int

    @classmethod
    def from_file(cls, path: str) -> "LlmConfig":
        payload = load_json(path)
        return cls(
            provider=payload.get("provider", "openai"),
            model=payload["model"],
            api_key_env=payload.get("api_key_env", "OPENAI_API_KEY"),
            temperature=float(payload.get("temperature", 0.1)),
            max_output_tokens=int(payload.get("max_output_tokens", 1000)),
        )


class OpenAiResponsesClient:
    def __init__(self, config: LlmConfig) -> None:
        if config.provider != "openai":
            raise ValueError(f"Unsupported provider for MVP: {config.provider}")
        self.config = config

    def test_connection(self, prompt: str = "Reply with only: API_OK") -> str:
        return self.generate_text(prompt)

    def generate_text(self, prompt: str) -> str:
        api_key = _get_api_key(self.config.api_key_env)
        if not api_key:
            raise RuntimeError(
                f"Missing API key. Set environment variable {self.config.api_key_env} before running this command."
            )

        payload = {
            "model": self.config.model,
            "input": prompt,
            "temperature": self.config.temperature,
            "max_output_tokens": self.config.max_output_tokens,
        }
        request = urllib.request.Request(
            "https://api.openai.com/v1/responses",
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            method="POST",
        )

        try:
            with urllib.request.urlopen(request, timeout=60) as response:
                body = json.loads(response.read().decode("utf-8"))
        except urllib.error.HTTPError as error:
            error_body = error.read().decode("utf-8", errors="replace")
            raise RuntimeError(f"OpenAI API returned HTTP {error.code}: {error_body}") from error

        return _extract_text(body) or json.dumps(body, indent=2)


class GeminiGenerateContentClient:
    def __init__(self, config: LlmConfig) -> None:
        if config.provider != "gemini":
            raise ValueError(f"Unsupported provider for Gemini client: {config.provider}")
        self.config = config

    def test_connection(self, prompt: str = "Reply with only: API_OK") -> str:
        return self.generate_text(prompt)

    def generate_text(self, prompt: str) -> str:
        api_key = _get_api_key(self.config.api_key_env)
        if not api_key:
            raise RuntimeError(
                f"Missing API key. Set environment variable {self.config.api_key_env} before running this command."
            )

        payload = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {
                "temperature": self.config.temperature,
                "maxOutputTokens": self.config.max_output_tokens,
            },
        }
        url = (
            "https://generativelanguage.googleapis.com/v1beta/models/"
            f"{self.config.model}:generateContent?key={api_key}"
        )
        request = urllib.request.Request(
            url,
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )

        try:
            with urllib.request.urlopen(request, timeout=60) as response:
                body = json.loads(response.read().decode("utf-8"))
        except urllib.error.HTTPError as error:
            error_body = error.read().decode("utf-8", errors="replace")
            raise RuntimeError(f"Gemini API returned HTTP {error.code}: {error_body}") from error

        return _extract_gemini_text(body) or json.dumps(body, indent=2)


def build_llm_client(config: LlmConfig) -> OpenAiResponsesClient | GeminiGenerateContentClient:
    if config.provider == "openai":
        return OpenAiResponsesClient(config)
    if config.provider == "gemini":
        return GeminiGenerateContentClient(config)
    raise ValueError(f"Unsupported LLM provider: {config.provider}")


def _get_api_key(env_name: str) -> str | None:
    return os.environ.get(env_name) or _read_dotenv_value(env_name)


def _read_dotenv_value(name: str) -> str | None:
    dotenv_path = ".env"
    if not os.path.exists(dotenv_path):
        return None

    with open(dotenv_path, "r", encoding="utf-8") as file:
        for line in file:
            stripped = line.strip()
            if not stripped or stripped.startswith("#") or "=" not in stripped:
                continue
            key, value = stripped.split("=", 1)
            if key.strip() == name:
                return value.strip().strip('"').strip("'")
    return None


def _extract_text(payload: dict[str, Any]) -> str:
    texts: list[str] = []
    for output_item in payload.get("output", []):
        for content_item in output_item.get("content", []):
            if content_item.get("type") == "output_text":
                texts.append(content_item.get("text", ""))
    return "\n".join(text for text in texts if text).strip()


def _extract_gemini_text(payload: dict[str, Any]) -> str:
    texts: list[str] = []
    for candidate in payload.get("candidates", []):
        content = candidate.get("content", {})
        for part in content.get("parts", []):
            if "text" in part:
                texts.append(part["text"])
    return "\n".join(text for text in texts if text).strip()
