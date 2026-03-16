from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class SensorReading(BaseModel):
    timestamp: str
    temperature_c: float = Field(ge=-50, le=60)
    humidity_pct: float | None = Field(default=None, ge=0, le=100)


class IncidentInput(BaseModel):
    clinic_id: str = Field(min_length=1)
    region: str = Field(min_length=1)
    storage_unit_id: str = Field(min_length=1)
    stock_level_vials: int = Field(ge=0)
    expected_daily_demand: int = Field(ge=0)
    maintenance_backlog_days: int = Field(default=0, ge=0)
    portal_url: str = ""
    sensor_readings: list[SensorReading] = Field(default_factory=list)
    image_notes: list[str] = Field(default_factory=list)
    voice_transcript: str = ""


class AgentTrace(BaseModel):
    agent: str
    summary: str
    evidence: dict[str, Any] = Field(default_factory=dict)


class IncidentReport(BaseModel):
    severity: str
    risk_score: float
    confidence_score: float
    executive_summary: str
    root_causes: list[str]
    recommended_actions: list[str]
    automation_plan: list[str]
    data_quality_warnings: list[str]
    evidence: dict[str, Any]
    traces: list[AgentTrace]
