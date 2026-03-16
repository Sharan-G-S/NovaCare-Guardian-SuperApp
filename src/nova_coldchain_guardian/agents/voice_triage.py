from __future__ import annotations

from dataclasses import dataclass

from nova_coldchain_guardian.adapters.nova_client import NovaClient
from nova_coldchain_guardian.models import AgentTrace, IncidentInput


@dataclass
class VoiceTriageAgent:
    client: NovaClient

    def run(self, payload: IncidentInput) -> tuple[dict, AgentTrace]:
        transcript = (payload.voice_transcript or "").strip()
        if not transcript:
            result = {
                "risk_delta": 0,
                "flags": ["No voice transcript supplied"],
                "summary": "Voice triage skipped",
            }
            return result, AgentTrace(agent="voice_triage", summary=result["summary"], evidence=result)

        text = transcript.lower()
        urgency_map = {
            "power cut": 20,
            "compressor": 15,
            "temperature alarm": 20,
            "not cooling": 20,
            "vaccine wasted": 25,
            "delay": 10,
        }

        risk_delta = sum(score for phrase, score in urgency_map.items() if phrase in text)
        risk_delta = min(risk_delta, 35)
        flags = [phrase for phrase in urgency_map if phrase in text]

        system_prompt = "You are a voice triage agent for maintenance escalation."
        user_prompt = f"Extract urgency, root cause clues, and required next action from this transcript: {transcript}"
        summary = self.client.reason(system_prompt, user_prompt, mode="text")

        result = {
            "risk_delta": risk_delta,
            "flags": flags or ["No high-priority voice flags detected"],
            "summary": summary,
        }
        trace = AgentTrace(agent="voice_triage", summary=summary, evidence=result)
        return result, trace
