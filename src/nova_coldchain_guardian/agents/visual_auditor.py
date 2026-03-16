from __future__ import annotations

from dataclasses import dataclass

from nova_coldchain_guardian.adapters.nova_client import NovaClient
from nova_coldchain_guardian.models import AgentTrace, IncidentInput


@dataclass
class VisualAuditorAgent:
    client: NovaClient

    def run(self, payload: IncidentInput) -> tuple[dict, AgentTrace]:
        if not payload.image_notes:
            result = {
                "risk_delta": 0,
                "findings": ["No visual notes provided"],
                "summary": "Visual audit skipped due to missing evidence",
            }
            return result, AgentTrace(agent="visual_auditor", summary=result["summary"], evidence=result)

        flattened = " ".join(payload.image_notes).lower()
        keyword_hits = {
            "ice buildup": "cooling efficiency risk",
            "door seal": "air leak risk",
            "condensation": "humidity and insulation risk",
            "rust": "maintenance degradation risk",
            "alarm off": "monitoring disabled risk",
        }

        findings = [desc for key, desc in keyword_hits.items() if key in flattened]
        risk_delta = min(len(findings) * 10, 30)

        system_prompt = "You are a multimodal audit agent for cold chain inspections."
        user_prompt = (
            "Summarize likely refrigeration integrity issues from these visual inspection notes: "
            + " | ".join(payload.image_notes)
        )
        nova_summary = self.client.reason(system_prompt, user_prompt, mode="multimodal")

        result = {
            "risk_delta": risk_delta,
            "findings": findings or ["No high-risk visual keywords found"],
            "summary": nova_summary,
        }
        trace = AgentTrace(agent="visual_auditor", summary=nova_summary, evidence=result)
        return result, trace
