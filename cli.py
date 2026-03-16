from __future__ import annotations

import argparse
import json

from dotenv import load_dotenv

from nova_coldchain_guardian.config import project_root
from nova_coldchain_guardian.models import IncidentInput
from nova_coldchain_guardian.workflows.incident_response import IncidentResponseWorkflow


def run(sample: bool, file_path: str | None) -> int:
    load_dotenv()
    workflow = IncidentResponseWorkflow()

    if sample:
        path = project_root() / "data" / "sample" / "incident_event.json"
    elif file_path:
        path = project_root() / file_path
    else:
        raise ValueError("Use --sample or --file <path>")

    payload = IncidentInput.model_validate_json(path.read_text(encoding="utf-8"))
    report = workflow.execute(payload)
    print(report.model_dump_json(indent=2))
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Run Nova Cold Chain Guardian workflow")
    parser.add_argument("--sample", action="store_true", help="Run with sample incident input")
    parser.add_argument("--file", type=str, default=None, help="Path to incident json from project root")
    args = parser.parse_args()
    return run(sample=args.sample, file_path=args.file)


if __name__ == "__main__":
    raise SystemExit(main())
