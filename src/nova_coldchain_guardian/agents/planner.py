from __future__ import annotations

from dataclasses import dataclass

from nova_coldchain_guardian.adapters.nova_client import NovaClient
from nova_coldchain_guardian.models import AgentTrace, IncidentInput


@dataclass
class PlannerAgent:
    client: NovaClient

    def run(self, payload: IncidentInput) -> tuple[str, AgentTrace]:
        system_prompt = "You are a safety-critical planning agent for vaccine cold chain operations."
        user_prompt = (
            f"Create a short investigation plan for clinic {payload.clinic_id} in {payload.region}. "
            f"Storage unit: {payload.storage_unit_id}. "
            f"Sensor points: {len(payload.sensor_readings)}. "
            f"Image notes: {len(payload.image_notes)}. "
            f"Voice transcript length: {len(payload.voice_transcript)} characters."
        )
        plan = self.client.reason(system_prompt, user_prompt, mode="text")
        trace = AgentTrace(agent="planner", summary=plan, evidence={"clinic_id": payload.clinic_id})
        return plan, trace
