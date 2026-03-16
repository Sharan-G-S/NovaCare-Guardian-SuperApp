from __future__ import annotations

import json
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from nova_coldchain_guardian.config import project_root
from nova_coldchain_guardian.models import IncidentInput, IncidentReport
from nova_coldchain_guardian.workflows.incident_response import IncidentResponseWorkflow

load_dotenv()

app = FastAPI(title="NovaCare Guardian SuperApp", version="1.0.0")

# Mount Static and Templates
ui_path = project_root() / "src" / "ui"
app.mount("/static", StaticFiles(directory=str(ui_path / "static")), name="static")
templates = Jinja2Templates(directory=str(ui_path / "templates"))

workflow = IncidentResponseWorkflow()


@app.get("/")
async def serve_ui(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


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
