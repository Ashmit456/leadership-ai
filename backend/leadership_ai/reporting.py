from __future__ import annotations

from datetime import datetime
from typing import Any

from .models import AssessmentResult


def build_markdown_report(result: AssessmentResult) -> str:
    trace_lines = [f"- {step.node}: {step.summary}" for step in result.decision_trace]
    strengths = "\n".join(f"- {item}" for item in result.strengths)
    weaknesses = "\n".join(f"- {item}" for item in result.weaknesses)
    recommendations = "\n".join(f"- {item}" for item in result.recommendations)

    return f"""# Leadership Assessment Report

## Candidate
- Name: {result.employee.full_name}
- Employee ID: {result.employee.employee_id}
- Department: {result.employee.department}
- Tier: {result.tier.value}
- Score: {result.leadership_score}
- Confidence: {result.confidence}

## Strengths
{strengths}

## Weaknesses
{weaknesses}

## Recommendations
{recommendations}

## Decision Trace
{chr(10).join(trace_lines)}

Generated at {datetime.utcnow().isoformat()}Z
"""


def build_chart_payload(result: AssessmentResult) -> dict[str, Any]:
    radar = [
        {"axis": "Execution", "value": result.chart_payload["signals"]["execution"]},
        {"axis": "Influence", "value": result.chart_payload["signals"]["influence"]},
        {"axis": "Growth", "value": result.chart_payload["signals"]["growth"]},
        {"axis": "Team", "value": result.chart_payload["signals"]["team"]},
        {"axis": "Text", "value": result.chart_payload["signals"]["text"]},
    ]
    contribution_bars = [
        {"label": item.feature.replace("_", " ").title(), "value": round(item.impact, 2)}
        for item in result.feature_contributions[:6]
    ]
    return {
        "radar": radar,
        "contributions": contribution_bars,
        "score": result.leadership_score,
        "tier": result.tier.value,
    }
