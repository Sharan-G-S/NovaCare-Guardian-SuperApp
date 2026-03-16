from __future__ import annotations

from dataclasses import dataclass


@dataclass
class UIAutomationAdapter:
    def build_actions(self, portal_url: str, severity: str, clinic_id: str) -> list[str]:
        base = portal_url or "operations portal"
        actions = [
            f"Open {base} and create incident for clinic {clinic_id}",
            "Attach risk report and evidence bundle",
        ]

        if severity in {"high", "critical"}:
            actions.extend(
                [
                    "Trigger urgent maintenance workflow",
                    "Escalate to district cold chain coordinator",
                ]
            )
        else:
            actions.append("Create preventive maintenance task")

        return actions
