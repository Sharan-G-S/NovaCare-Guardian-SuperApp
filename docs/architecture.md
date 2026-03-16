System Architecture
===================

I designed this project as an agentic safety system with clear separation of concerns.

Core Design Principles
----------------------

- deterministic policy checks for reliability
- model abstraction so I can switch Nova model versions safely
- composable agents so I can add or replace capabilities without breaking the workflow
- API-first deployment model for integration into health operations systems

Agent Workflow
--------------

1. Planner Agent creates an investigation plan and context framing
2. Sensor Analyst Agent scores thermal and telemetry risk
3. Visual Auditor Agent extracts physical failure signals from visual evidence notes
4. Voice Triage Agent extracts urgency and fault clues from technician speech transcripts
5. Policy Checker Agent combines all evidence into a transparent risk score and severity class
6. Action Executor Agent produces operating instructions and UI automation tasks

Deployment Blueprint
--------------------

- Inference Layer: Amazon Nova models on AWS
- Agent Orchestration Layer: Python service with modular agents
- Workflow Automation Layer: Nova Act or equivalent UI automation pipeline
- Operations Layer: existing health portals, ticketing, and monitoring channels

Production Hardening Path
-------------------------

- add event-driven ingestion using queues
- persist reports and traces for auditability
- add role-based access control
- attach real image and audio files in multimodal calls
- add online evaluation for false positives and missed incidents
