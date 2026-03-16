from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Settings:
    aws_region: str
    nova_text_model_id: str
    nova_multimodal_model_id: str
    enable_live_nova: bool


def get_settings() -> Settings:
    return Settings(
        aws_region=os.getenv("AWS_REGION", "us-east-1"),
        nova_text_model_id=os.getenv("NOVA_TEXT_MODEL_ID", "amazon.nova-lite-v1:0"),
        nova_multimodal_model_id=os.getenv("NOVA_MULTIMODAL_MODEL_ID", "amazon.nova-lite-v1:0"),
        enable_live_nova=os.getenv("ENABLE_LIVE_NOVA", "false").lower() == "true",
    )


def project_root() -> Path:
    return Path(__file__).resolve().parents[2]
