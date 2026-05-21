from __future__ import annotations

from copy import deepcopy
from typing import Any

from .models import EmployeeProfile


NUMERIC_FIELDS = [
    "performance_score",
    "peer_feedback_score",
    "manager_feedback_score",
    "collaboration_score",
    "communication_score",
    "problem_solving_score",
    "initiative_score",
    "adaptability_score",
    "learning_agility_score",
    "people_influence_score",
    "decision_quality_score",
    "project_delivery_score",
    "engagement_score",
]


DEFAULTS = {
    "department": "Unknown",
    "job_family": "Unknown",
    "level": "IC3",
    "location": "Hybrid",
    "sentiment_summary": "",
    "career_history": "",
    "manager_notes": "",
    "tenure_years": 3.0,
    "age": 34,
}


def _clamp(value: float, lower: float = 0.0, upper: float = 100.0) -> float:
    return max(lower, min(upper, float(value)))


def canonicalize_employee(employee: EmployeeProfile | dict[str, Any]) -> EmployeeProfile:
    if isinstance(employee, EmployeeProfile):
        return employee
    payload = deepcopy(employee)
    for field, default in DEFAULTS.items():
        payload.setdefault(field, default)
    for field in NUMERIC_FIELDS:
        if payload.get(field) is None:
            payload[field] = 50.0
        payload[field] = _clamp(payload[field])
    payload["tenure_years"] = max(0.0, float(payload.get("tenure_years", 3.0)))
    age = payload.get("age")
    if age is not None:
        payload["age"] = int(max(18, min(70, int(age))))
    return EmployeeProfile.model_validate(payload)


def profile_quality_checks(profile: EmployeeProfile) -> dict[str, Any]:
    missing = [field for field, value in profile.model_dump().items() if value in (None, "")]
    outlier_flags = {
        "very_short_tenure": profile.tenure_years < 0.5,
        "new_manager": profile.level.lower().startswith("manager") and profile.tenure_years < 2,
        "young_high_tenure": bool(profile.age and profile.age < 24 and profile.tenure_years > 5),
    }
    return {
        "missing_fields": missing,
        "outlier_flags": outlier_flags,
        "missing_count": len(missing),
        "completeness": round(1.0 - len(missing) / len(profile.model_fields), 3),
    }


def preprocess_employee(employee: EmployeeProfile | dict[str, Any]) -> tuple[EmployeeProfile, dict[str, Any]]:
    profile = canonicalize_employee(employee)
    checks = profile_quality_checks(profile)
    return profile, checks
