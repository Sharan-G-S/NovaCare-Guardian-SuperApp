from __future__ import annotations

from dataclasses import dataclass

from nova_coldchain_guardian.adapters.ui_automation import UIAutomationAdapter
from nova_coldchain_guardian.models import AgentTrace, IncidentInput


@dataclass
class ActionExecutorAgent:
    ui_adapter: UIAutomationAdapter

    def run(self, payload: IncidentInput, policy_result: dict) -> tuple[dict, AgentTrace]:
        severity = policy_result["severity"]
        actions: list[str] = []

        if severity == "critical":
            actions.extend(
                [
                    "Quarantine exposed vaccine lots immediately",
                    "Deploy backup cold storage within 2 hours",
                    "Notify district immunization command center",
                ]
            )
        elif severity == "high":
            actions.extend(
                [
                    "Run emergency refrigerator diagnostics",
                    "Increase temperature polling frequency",
                    "Dispatch maintenance team in same shift",
                ]
            )
        elif severity == "medium":
            actions.extend(
                [
                    "Schedule preventive maintenance within 24 hours",
                    "Cross-check manual thermometer logs",
                ]
            )
        else:
            actions.extend(
                [
                    "Continue standard monitoring",
                    "Include findings in weekly compliance review",
                ]
            )

        confidence_score = float(policy_result.get("confidence_score", 1.0))
        if confidence_score < 0.75:
            actions.append("Collect missing evidence before closure and rerun triage")

        automation = self.ui_adapter.build_actions(
            portal_url=payload.portal_url,
            severity=severity,
            clinic_id=payload.clinic_id,
        )

        result = {
            "recommended_actions": actions,
            "automation_plan": automation,
            "severity": severity,
        }
        trace = AgentTrace(
            agent="action_executor",
            summary=f"Prepared {len(actions)} operational actions and {len(automation)} automation steps",
            evidence=result,
        )
        return result, trace
