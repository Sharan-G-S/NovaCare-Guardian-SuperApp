from __future__ import annotations

from dataclasses import dataclass

from nova_coldchain_guardian.models import AgentTrace, IncidentInput


@dataclass
class SensorAnalystAgent:
    rules: dict

    def run(self, payload: IncidentInput) -> tuple[dict, AgentTrace]:
        threshold = float(self.rules["temperature_breach_c"])
        readings = payload.sensor_readings

        if not readings:
            result = {
                "max_temp": None,
                "avg_temp": None,
                "breach_count": 0,
                "sustained_breach_max": 0,
                "risk_delta": 20,
                "sensor_summary": "No sensor readings available",
            }
            trace = AgentTrace(agent="sensor_analyst", summary=result["sensor_summary"], evidence=result)
            return result, trace

        temperatures = [entry.temperature_c for entry in readings]
        max_temp = max(temperatures)
        avg_temp = sum(temperatures) / len(temperatures)
        breach_count = sum(1 for temp in temperatures if temp > threshold)

        sustained_breach_max = 0
        current_streak = 0
        for temp in temperatures:
            if temp > threshold:
                current_streak += 1
                sustained_breach_max = max(sustained_breach_max, current_streak)
            else:
                current_streak = 0

        risk_delta = 0
        if breach_count >= 1:
            risk_delta += 25
        if breach_count >= 3:
            risk_delta += 15
        if max_temp >= threshold + 2:
            risk_delta += 20
        if sustained_breach_max >= 2:
            risk_delta += 10
        if avg_temp >= threshold - 0.5:
            risk_delta += 5

        summary = (
            f"Observed max temperature {max_temp:.1f}C with {breach_count} breach events above {threshold:.1f}C"
        )
        result = {
            "max_temp": max_temp,
            "avg_temp": round(avg_temp, 2),
            "breach_count": breach_count,
            "sustained_breach_max": sustained_breach_max,
            "risk_delta": risk_delta,
            "sensor_summary": summary,
        }
        trace = AgentTrace(agent="sensor_analyst", summary=summary, evidence=result)
        return result, trace
