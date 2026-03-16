from __future__ import annotations

import json

from dotenv import load_dotenv
from fastapi import FastAPI

from nova_coldchain_guardian.config import project_root
from nova_coldchain_guardian.models import IncidentInput, IncidentReport
from nova_coldchain_guardian.workflows.incident_response import IncidentResponseWorkflow

load_dotenv()

app = FastAPI(title="Nova Cold Chain Guardian", version="0.1.0")
workflow = IncidentResponseWorkflow()


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.post("/analyze", response_model=IncidentReport)
def analyze(payload: IncidentInput) -> IncidentReport:
    return workflow.execute(payload)


@app.post("/simulate", response_model=IncidentReport)
def simulate() -> IncidentReport:
    sample_path = project_root() / "data" / "sample" / "incident_event.json"
    data = json.loads(sample_path.read_text(encoding="utf-8"))
    payload = IncidentInput.model_validate(data)
    return workflow.execute(payload)
