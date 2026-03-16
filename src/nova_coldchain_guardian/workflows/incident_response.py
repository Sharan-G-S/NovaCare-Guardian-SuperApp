from __future__ import annotations

from nova_coldchain_guardian.config import get_settings, project_root
from nova_coldchain_guardian.models import IncidentInput, IncidentReport
from nova_coldchain_guardian.orchestrator import IncidentOrchestrator


class IncidentResponseWorkflow:
    def __init__(self) -> None:
        settings = get_settings()
        rules_path = project_root() / "src" / "nova_coldchain_guardian" / "config" / "policy_rules.yaml"
        self.orchestrator = IncidentOrchestrator(settings=settings, rules_path=rules_path)

    def execute(self, payload: IncidentInput) -> IncidentReport:
        return self.orchestrator.run(payload)
