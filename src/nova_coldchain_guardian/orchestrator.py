from __future__ import annotations

from pathlib import Path

from nova_coldchain_guardian.adapters.nova_client import BedrockNovaClient, MockNovaClient, NovaClient
from nova_coldchain_guardian.adapters.ui_automation import UIAutomationAdapter
from nova_coldchain_guardian.agents.action_executor import ActionExecutorAgent
from nova_coldchain_guardian.agents.planner import PlannerAgent
from nova_coldchain_guardian.agents.policy_checker import PolicyCheckerAgent
from nova_coldchain_guardian.agents.sensor_analyst import SensorAnalystAgent
from nova_coldchain_guardian.agents.visual_auditor import VisualAuditorAgent
from nova_coldchain_guardian.agents.voice_triage import VoiceTriageAgent
from nova_coldchain_guardian.config import Settings
from nova_coldchain_guardian.models import IncidentInput, IncidentReport
from nova_coldchain_guardian.rules import load_rules


class IncidentOrchestrator:
    def __init__(self, settings: Settings, rules_path: Path) -> None:
        rules = load_rules(rules_path)
        client: NovaClient

        if settings.enable_live_nova:
            client = BedrockNovaClient(
                region=settings.aws_region,
                text_model_id=settings.nova_text_model_id,
                multimodal_model_id=settings.nova_multimodal_model_id,
            )
        else:
            client = MockNovaClient()

        self.planner = PlannerAgent(client=client)
        self.sensor = SensorAnalystAgent(rules=rules)
        self.visual = VisualAuditorAgent(client=client)
        self.voice = VoiceTriageAgent(client=client)
        self.policy = PolicyCheckerAgent(rules=rules)
        self.action = ActionExecutorAgent(ui_adapter=UIAutomationAdapter())

    def run(self, payload: IncidentInput) -> IncidentReport:
        traces = []

        plan, planner_trace = self.planner.run(payload)
        traces.append(planner_trace)

        sensor_result, sensor_trace = self.sensor.run(payload)
        traces.append(sensor_trace)

        visual_result, visual_trace = self.visual.run(payload)
        traces.append(visual_trace)

        voice_result, voice_trace = self.voice.run(payload)
        traces.append(voice_trace)

        policy_result, policy_trace = self.policy.run(payload, sensor_result, visual_result, voice_result)
        traces.append(policy_trace)

        action_result, action_trace = self.action.run(payload, policy_result)
        traces.append(action_trace)

        root_causes = policy_result.get("causes", [])
        confidence_score = float(policy_result.get("confidence_score", 0.8))
        data_quality_warnings = policy_result.get("data_quality_warnings", [])
        executive_summary = (
            f"I used a multi-agent Nova workflow to evaluate clinic {payload.clinic_id}. "
            f"Final severity is {policy_result['severity']} with risk score {policy_result['risk_score']:.1f}. "
            f"Confidence score is {confidence_score:.2f}. "
            f"Planner output: {plan[:220]}"
        )

        evidence = {
            "sensor": sensor_result,
            "visual": visual_result,
            "voice": voice_result,
            "policy": policy_result,
        }

        return IncidentReport(
            severity=policy_result["severity"],
            risk_score=policy_result["risk_score"],
            confidence_score=confidence_score,
            executive_summary=executive_summary,
            root_causes=root_causes,
            recommended_actions=action_result["recommended_actions"],
            automation_plan=action_result["automation_plan"],
            data_quality_warnings=data_quality_warnings,
            evidence=evidence,
            traces=traces,
        )
