from __future__ import annotations

from collections import Counter
from math import log1p
from typing import Any

from .models import EmployeeProfile


POSITIVE_KEYWORDS = {
    "ownership",
    "influence",
    "collaborative",
    "growth",
    "accountability",
    "mentoring",
    "coach",
    "clear",
    "trusted",
    "leadership",
    "resilient",
    "strategic",
}

NEGATIVE_KEYWORDS = {"delay", "escalation", "issue", "risk", "missed", "blocker", "conflict", "unclear"}


def _tokenize(text: str) -> Counter:
    tokens = [token.strip(".,;:!?()[]{}\"'`").lower() for token in text.split()]
    return Counter(token for token in tokens if token)


def text_signal(summary: str) -> dict[str, Any]:
    tokens = _tokenize(summary)
    positive_hits = sum(tokens[word] for word in POSITIVE_KEYWORDS)
    negative_hits = sum(tokens[word] for word in NEGATIVE_KEYWORDS)
    score = 50.0 + 8.0 * log1p(positive_hits) - 7.0 * log1p(negative_hits)
    return {
        "positive_hits": positive_hits,
        "negative_hits": negative_hits,
        "text_signal": max(0.0, min(100.0, round(score, 2))),
    }


def derive_features(profile: EmployeeProfile) -> dict[str, Any]:
    team_signal = round(
        0.36 * profile.collaboration_score
        + 0.28 * profile.communication_score
        + 0.36 * profile.people_influence_score,
        2,
    )
    execution_signal = round(
        0.34 * profile.performance_score
        + 0.33 * profile.project_delivery_score
        + 0.33 * profile.decision_quality_score,
        2,
    )
    growth_signal = round(
        0.37 * profile.learning_agility_score
        + 0.33 * profile.adaptability_score
        + 0.30 * profile.initiative_score,
        2,
    )
    influence_signal = round(
        0.4 * profile.people_influence_score
        + 0.3 * profile.manager_feedback_score
        + 0.3 * profile.peer_feedback_score,
        2,
    )
    text_features = text_signal(profile.sentiment_summary + " " + profile.manager_notes + " " + profile.career_history)

    tenure_factor = min(1.25, 0.6 + profile.tenure_years / 8)
    readiness_band = "early" if profile.tenure_years < 2 else "mid" if profile.tenure_years < 6 else "senior"

    return {
        "team_signal": team_signal,
        "execution_signal": execution_signal,
        "growth_signal": growth_signal,
        "influence_signal": influence_signal,
        "text_features": text_features,
        "tenure_factor": round(tenure_factor, 3),
        "readiness_band": readiness_band,
        "leadership_shape": {
            "execution": execution_signal,
            "influence": influence_signal,
            "growth": growth_signal,
            "team": team_signal,
        },
    }
