from __future__ import annotations

import json

from nova_coldchain_guardian.config import get_settings, project_root
from nova_coldchain_guardian.models import IncidentInput
from nova_coldchain_guardian.orchestrator import IncidentOrchestrator


def test_sample_incident_reaches_high_or_critical_risk() -> None:
    settings = get_settings()
    rules_path = project_root() / "src" / "nova_coldchain_guardian" / "config" / "policy_rules.yaml"
    orchestrator = IncidentOrchestrator(settings=settings, rules_path=rules_path)

    sample_path = project_root() / "data" / "sample" / "incident_event.json"
    payload = IncidentInput.model_validate_json(sample_path.read_text(encoding="utf-8"))

    report = orchestrator.run(payload)

    assert report.severity in {"high", "critical"}
    assert report.risk_score >= 70
    assert 0.3 <= report.confidence_score <= 1.0
    assert len(report.recommended_actions) >= 2
    assert len(report.automation_plan) >= 2
    assert any(trace.agent == "policy_checker" for trace in report.traces)


def test_low_risk_payload_stays_below_high() -> None:
    settings = get_settings()
    rules_path = project_root() / "src" / "nova_coldchain_guardian" / "config" / "policy_rules.yaml"
    orchestrator = IncidentOrchestrator(settings=settings, rules_path=rules_path)

    payload_dict = {
        "clinic_id": "CLINIC-LOW-01",
        "region": "Test Region",
        "storage_unit_id": "UNIT-01",
        "stock_level_vials": 1800,
        "expected_daily_demand": 120,
        "maintenance_backlog_days": 1,
        "portal_url": "",
        "sensor_readings": [
            {"timestamp": "2026-03-16T06:00:00Z", "temperature_c": 5.1},
            {"timestamp": "2026-03-16T07:00:00Z", "temperature_c": 5.4},
            {"timestamp": "2026-03-16T08:00:00Z", "temperature_c": 5.3}
        ],
        "image_notes": ["Clean interior and stable indicator lights"],
        "voice_transcript": "Routine inspection completed, no anomalies observed"
    }

    payload = IncidentInput.model_validate(payload_dict)
    report = orchestrator.run(payload)

    assert report.severity in {"low", "medium"}
    assert report.risk_score < 70
    assert report.confidence_score >= 0.8


def test_sparse_evidence_reduces_confidence_and_adds_recheck_action() -> None:
    settings = get_settings()
    rules_path = project_root() / "src" / "nova_coldchain_guardian" / "config" / "policy_rules.yaml"
    orchestrator = IncidentOrchestrator(settings=settings, rules_path=rules_path)

    payload_dict = {
        "clinic_id": "CLINIC-SPARSE-01",
        "region": "Remote Delta",
        "storage_unit_id": "UNIT-EDGE-03",
        "stock_level_vials": 300,
        "expected_daily_demand": 80,
        "maintenance_backlog_days": 0,
        "portal_url": "",
        "sensor_readings": [],
        "image_notes": [],
        "voice_transcript": ""
    }

    payload = IncidentInput.model_validate(payload_dict)
    report = orchestrator.run(payload)

    assert report.confidence_score < 0.7
    assert len(report.data_quality_warnings) >= 2
    assert any("Collect missing evidence" in action for action in report.recommended_actions)
