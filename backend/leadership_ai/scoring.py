from __future__ import annotations

from math import tanh
from typing import Any

from .models import AssessmentTier, FeatureContribution, EmployeeProfile


WEIGHTS = {
    "performance_score": 0.12,
    "manager_feedback_score": 0.12,
    "initiative_score": 0.10,
    "people_influence_score": 0.11,
    "learning_agility_score": 0.10,
    "collaboration_score": 0.09,
    "communication_score": 0.08,
    "decision_quality_score": 0.08,
    "project_delivery_score": 0.08,
    "adaptability_score": 0.07,
    "peer_feedback_score": 0.05,
    "text_signal": 0.04,
    "tenure_factor": 0.03,
    "engagement_score": 0.03,
}


def _normalize(value: float) -> float:
    return max(0.0, min(1.0, value / 100.0))


def _tier_for_score(score: float) -> AssessmentTier:
    if score >= 88:
        return AssessmentTier.future_leader
    if score >= 74:
        return AssessmentTier.high_potential
    if score >= 58:
        return AssessmentTier.ready
    return AssessmentTier.emerging


def _confidence_from_completeness(completeness: float, agreement: float) -> float:
    return round(max(0.42, min(0.97, 0.4 + 0.35 * completeness + 0.25 * agreement)), 3)


def score_leadership(profile: EmployeeProfile, features: dict[str, Any], validation: dict[str, Any]) -> dict[str, Any]:
    raw_signals = {
        "performance_score": profile.performance_score,
        "manager_feedback_score": profile.manager_feedback_score,
        "initiative_score": profile.initiative_score,
        "people_influence_score": profile.people_influence_score,
        "learning_agility_score": profile.learning_agility_score,
        "collaboration_score": profile.collaboration_score,
        "communication_score": profile.communication_score,
        "decision_quality_score": profile.decision_quality_score,
        "project_delivery_score": profile.project_delivery_score,
        "adaptability_score": profile.adaptability_score,
        "peer_feedback_score": profile.peer_feedback_score,
        "text_signal": features["text_features"]["text_signal"],
        "tenure_factor": features["tenure_factor"] * 100,
        "engagement_score": profile.engagement_score,
    }

    weighted_sum = 0.0
    contributions: list[FeatureContribution] = []
    for feature, weight in WEIGHTS.items():
        normalized = _normalize(raw_signals[feature])
        impact = (normalized - 0.5) * weight * 100
        weighted_sum += normalized * weight
        contributions.append(
            FeatureContribution(
                feature=feature,
                value=round(raw_signals[feature], 2),
                impact=round(impact, 3),
                direction="positive" if impact > 0 else "negative" if impact < 0 else "neutral",
            )
        )

    shape_boost = 0.05 * tanh((features["growth_signal"] - 55.0) / 16.0)
    shape_boost += 0.05 * tanh((features["team_signal"] - 55.0) / 16.0)
    shape_boost += 0.04 * tanh((features["influence_signal"] - 55.0) / 16.0)

    score = round(max(0.0, min(100.0, (weighted_sum + shape_boost + 0.16) * 100)), 2)
    tier = _tier_for_score(score)
    completeness = validation.get("completeness", 1.0)
    agreement = 1.0 - min(1.0, abs(features["execution_signal"] - features["influence_signal"]) / 140.0)
    confidence = _confidence_from_completeness(completeness, agreement)

    sorted_contribs = sorted(contributions, key=lambda item: abs(item.impact), reverse=True)

    return {
        "leadership_score": score,
        "tier": tier,
        "confidence": confidence,
        "feature_contributions": sorted_contribs,
        "raw_signals": raw_signals,
        "signal_breakdown": {
            "execution": round(features["execution_signal"], 2),
            "influence": round(features["influence_signal"], 2),
            "growth": round(features["growth_signal"], 2),
            "team": round(features["team_signal"], 2),
        },
    }
