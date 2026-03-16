from __future__ import annotations

from dataclasses import dataclass

from nova_coldchain_guardian.models import AgentTrace, IncidentInput


@dataclass
class PolicyCheckerAgent:
    rules: dict

    def run(self, payload: IncidentInput, sensor_result: dict, visual_result: dict, voice_result: dict) -> tuple[dict, AgentTrace]:
        risk_score = 10
        causes: list[str] = []
        data_quality_warnings: list[str] = []
        confidence_score = 1.0

        risk_score += int(sensor_result.get("risk_delta", 0))
        risk_score += int(visual_result.get("risk_delta", 0))
        risk_score += int(voice_result.get("risk_delta", 0))

        if not payload.sensor_readings:
            data_quality_warnings.append("Sensor telemetry is missing")
            confidence_score -= 0.15
        if not payload.image_notes:
            data_quality_warnings.append("Visual inspection evidence is missing")
            confidence_score -= 0.12
        if not payload.voice_transcript.strip():
            data_quality_warnings.append("Voice technician evidence is missing")
            confidence_score -= 0.12

        demand = max(payload.expected_daily_demand, 1)
        stock_days = payload.stock_level_vials / demand

        if stock_days <= float(self.rules["critical_stock_days"]):
            risk_score += 15
            causes.append("Low vaccine stock coverage window")

        if payload.maintenance_backlog_days >= int(self.rules["backlog_days_alert"]):
            risk_score += 10
            causes.append("Maintenance backlog above policy threshold")

        if sensor_result.get("breach_count", 0) > 0:
            causes.append("Temperature excursions detected")

        for finding in visual_result.get("findings", []):
            if "risk" in finding:
                causes.append(finding)

        for flag in voice_result.get("flags", []):
            if flag not in {"No high-priority voice flags detected", "No voice transcript supplied"}:
                causes.append(f"Voice flag: {flag}")

        if sensor_result.get("breach_count", 0) >= 3 and not causes:
            data_quality_warnings.append("High sensor risk detected with weak corroborating evidence")
            confidence_score -= 0.2

        if not causes:
            causes.append("No direct policy breach detected")

        risk_score = min(risk_score, 100)
        confidence_score = max(0.3, min(1.0, confidence_score))

        if risk_score >= 85:
            severity = "critical"
        elif risk_score >= int(self.rules["high_risk_score"]):
            severity = "high"
        elif risk_score >= 45:
            severity = "medium"
        else:
            severity = "low"

        causes = list(dict.fromkeys(causes))
        summary = f"Policy checker set severity to {severity} with risk score {risk_score}"
        result = {
            "severity": severity,
            "risk_score": float(risk_score),
            "confidence_score": round(confidence_score, 2),
            "causes": causes,
            "data_quality_warnings": data_quality_warnings,
            "stock_days": round(stock_days, 2),
        }
        trace = AgentTrace(agent="policy_checker", summary=summary, evidence=result)
        return result, trace
