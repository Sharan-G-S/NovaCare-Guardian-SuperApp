Architecture One Pager
======================

System Goal
-----------
I ingest fragmented cold-chain incident evidence and produce an explainable, actionable response plan in one workflow run.

Core Components
---------------
- Ingestion Layer: incident payload with telemetry, inspection notes, and voice transcript.
- Orchestration Layer: ordered execution of specialist agents.
- Intelligence Layer: Amazon Nova reasoning and multimodal interpretation.
- Policy Layer: deterministic severity and compliance scoring.
- Action Layer: operational recommendations and automation handoff steps.

Agent Responsibilities
----------------------
- Planner: defines investigation strategy and context.
- Sensor Analyst: computes temperature breach profile.
- Visual Auditor: identifies physical integrity risks.
- Voice Triage: extracts urgency and causal clues.
- Policy Checker: fuses evidence into final severity with rationale.
- Action Executor: maps severity into concrete response operations.

Reliability Design
------------------
- Missing evidence penalties with explicit trace output.
- Contradictory evidence detection and confidence moderation.
- Deterministic policy thresholds for auditability.
- Bounded risk scoring to avoid uncontrolled escalation.

Production Path
---------------
- Add asynchronous queue ingestion.
- Store incident traces for audit and retraining feedback.
- Integrate with district operations portal and maintenance ticketing.
- Add observability dashboards for false-positive and miss tracking.
