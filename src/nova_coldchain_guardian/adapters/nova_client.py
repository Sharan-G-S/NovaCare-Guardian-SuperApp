from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol


class NovaClient(Protocol):
    def reason(self, system_prompt: str, user_prompt: str, mode: str = "text") -> str:
        ...


@dataclass
class MockNovaClient:
    def reason(self, system_prompt: str, user_prompt: str, mode: str = "text") -> str:
        trimmed = " ".join(user_prompt.split())
        return f"Simulated Nova output: {trimmed[:320]}"


@dataclass
class BedrockNovaClient:
    region: str
    text_model_id: str
    multimodal_model_id: str

    def __post_init__(self) -> None:
        try:
            import boto3
        except Exception as exc:
            raise RuntimeError("boto3 is required for live Nova calls") from exc

        self._client = boto3.client("bedrock-runtime", region_name=self.region)

    def reason(self, system_prompt: str, user_prompt: str, mode: str = "text") -> str:
        model_id = self.multimodal_model_id if mode == "multimodal" else self.text_model_id

        response = self._client.converse(
            modelId=model_id,
            system=[{"text": system_prompt}],
            messages=[{"role": "user", "content": [{"text": user_prompt}]}],
        )

        blocks = response.get("output", {}).get("message", {}).get("content", [])
        text_blocks = [block.get("text", "") for block in blocks if isinstance(block, dict)]
        merged = " ".join(part.strip() for part in text_blocks if part)
        return merged or "No textual response returned by Nova"
