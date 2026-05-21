from __future__ import annotations

from typing import Any

from .models import FeatureContribution


def _strength_or_gap(contribution: FeatureContribution) -> str:
    if contribution.direction == "positive":
        return f"{contribution.feature.replace('_', ' ').title()} is a strength"
    return f"{contribution.feature.replace('_', ' ').title()} needs attention"


def generate_explanation(
    profile_summary: dict[str, Any],
    scorecard: dict[str, Any],
    features: dict[str, Any],
) -> dict[str, Any]:
    ranked = scorecard["feature_contributions"]
    top_positive = [item for item in ranked if item.impact > 0][:3]
    top_negative = [item for item in reversed(ranked) if item.impact < 0][:3]

    strengths = [
        f"{item.feature.replace('_', ' ').title()} is driving the assessment positively"
        for item in top_positive
    ]
    weaknesses = [
        f"{item.feature.replace('_', ' ').title()} is constraining the score"
        for item in top_negative
    ]

    if not strengths:
        strengths = ["Core indicators are stable but not yet exceptional"]
    if not weaknesses:
        weaknesses = ["No major gaps were detected in the current profile"]

    recommendations = [
        "Assign cross-functional ownership for a high-visibility project.",
        "Increase coaching exposure to strengthen people leadership readiness.",
        "Pair with a senior sponsor to widen strategic decision-making context.",
    ]

    if features["growth_signal"] > 72:
        recommendations[1] = "Use a stretch assignment to convert strong learning agility into visible leadership evidence."
    if features["influence_signal"] < 54:
        recommendations[2] = "Create stakeholder-facing opportunities to build influence and executive presence."

    narrative = (
        f"{profile_summary['full_name']} demonstrates a {scorecard['tier'].value.lower()} profile with "
        f"execution strength at {features['execution_signal']:.1f}, influence at {features['influence_signal']:.1f}, "
        f"and growth at {features['growth_signal']:.1f}. "
        f"The decision trace favors balanced leadership signals over a single standout trait."
    )

    return {
        "strengths": strengths,
        "weaknesses": weaknesses,
        "recommendations": recommendations,
        "explanation": narrative,
        "ranked_contributions": ranked,
        "highlight_summary": {
            "positive": [_strength_or_gap(item) for item in top_positive],
            "negative": [_strength_or_gap(item) for item in top_negative],
        },
    }
