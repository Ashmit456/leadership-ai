from __future__ import annotations

from math import exp
from random import Random

from .models import EmployeeProfile


DEPARTMENTS = [
    ("Engineering", "Technical", 0.28),
    ("Product", "Business", 0.14),
    ("Sales", "Commercial", 0.13),
    ("Operations", "Operations", 0.12),
    ("Finance", "Business", 0.09),
    ("Customer Success", "Commercial", 0.10),
    ("HR", "People", 0.08),
    ("Marketing", "Creative", 0.06),
]

FIRST_NAMES = ["Aarav", "Isha", "Maya", "Noah", "Elena", "Priya", "Jordan", "Owen", "Asha", "Riya"]
LAST_NAMES = ["Sharma", "Patel", "Iyer", "Gupta", "Nair", "Kapoor", "Singh", "Mehta", "Rao", "Bose"]
LEVELS = ["IC2", "IC3", "IC4", "Manager", "Senior Manager"]
LOCATIONS = ["Hybrid", "Remote", "On-site"]


def _weighted_choice(rng: Random, choices: list[tuple[str, str, float]]) -> tuple[str, str]:
    threshold = rng.random()
    cumulative = 0.0
    for department, job_family, weight in choices:
        cumulative += weight
        if threshold <= cumulative:
            return department, job_family
    department, job_family, _ = choices[-1]
    return department, job_family


def _clamp(value: float, lower: float = 0.0, upper: float = 100.0) -> float:
    return round(max(lower, min(upper, value)), 2)


def _beta_like(rng: Random, alpha: float, beta: float) -> float:
    left = rng.gammavariate(alpha, 1.0)
    right = rng.gammavariate(beta, 1.0)
    return left / (left + right)


def _normal_like(rng: Random, mean: float, spread: float) -> float:
    return rng.gauss(mean, spread)


def _logistic(value: float) -> float:
    return 1.0 / (1.0 + exp(-value))


def generate_synthetic_employee(seed: int | None = None, index: int = 0) -> EmployeeProfile:
    rng = Random((seed or 0) + index * 97)
    department, job_family = _weighted_choice(rng, DEPARTMENTS)
    first_name = rng.choice(FIRST_NAMES)
    last_name = rng.choice(LAST_NAMES)
    location = rng.choice(LOCATIONS)

    latent_potential = _beta_like(rng, 2.4, 2.1)
    execution_strength = _beta_like(rng, 2.8, 1.9)
    social_strength = _beta_like(rng, 2.2, 2.2)
    growth_strength = _beta_like(rng, 2.0, 2.0)

    tenure_years = _clamp(_normal_like(rng, 4.8, 2.9), 0.1, 18.0)
    age = int(_clamp(_normal_like(rng, 34.0, 6.5), 22, 58))

    performance_score = _clamp(48 + 42 * execution_strength + rng.gauss(0, 7))
    peer_feedback_score = _clamp(50 + 38 * social_strength + rng.gauss(0, 8))
    manager_feedback_score = _clamp(46 + 45 * latent_potential + rng.gauss(0, 8))
    collaboration_score = _clamp(46 + 40 * social_strength + rng.gauss(0, 7))
    communication_score = _clamp(45 + 39 * social_strength + rng.gauss(0, 7))
    problem_solving_score = _clamp(47 + 40 * execution_strength + rng.gauss(0, 7))
    initiative_score = _clamp(42 + 46 * latent_potential + rng.gauss(0, 9))
    adaptability_score = _clamp(45 + 43 * growth_strength + rng.gauss(0, 8))
    learning_agility_score = _clamp(44 + 45 * growth_strength + rng.gauss(0, 8))
    people_influence_score = _clamp(40 + 50 * social_strength + rng.gauss(0, 8))
    decision_quality_score = _clamp(47 + 39 * execution_strength + rng.gauss(0, 7))
    project_delivery_score = _clamp(46 + 42 * execution_strength + rng.gauss(0, 7))
    engagement_score = _clamp(49 + 37 * latent_potential + rng.gauss(0, 7))

    summary = (
        f"Consistently demonstrates {rng.choice(['strong', 'solid', 'improving'])} ownership, "
        f"{rng.choice(['collaborative', 'clear', 'steady'])} communication, and "
        f"{rng.choice(['growing', 'high', 'balanced'])} cross-functional influence."
    )
    career_history = (
        f"Promoted once over the last {max(1, int(tenure_years // 2) + 1)} years with exposure to "
        f"{rng.choice(['project leadership', 'process design', 'stakeholder management', 'delivery execution'])}."
    )
    manager_notes = (
        f"Shows {rng.choice(['high curiosity', 'strong accountability', 'reliable follow-through', 'a constructive feedback mindset'])} "
        f"and is effective in {rng.choice(['ambiguity', 'fast-paced environments', 'cross-functional work', 'customer-facing situations'])}."
    )

    hidden_signal = (
        0.20 * (performance_score / 100)
        + 0.16 * (manager_feedback_score / 100)
        + 0.14 * (initiative_score / 100)
        + 0.12 * (people_influence_score / 100)
        + 0.12 * (learning_agility_score / 100)
        + 0.10 * (collaboration_score / 100)
        + 0.08 * (decision_quality_score / 100)
        + 0.08 * (engagement_score / 100)
        + 0.02 * (tenure_years / 10)
        - 0.04 * rng.random()
    )
    label_high_potential = _logistic((hidden_signal - 0.55) * 8) > 0.5

    level_index = 1 + int(tenure_years // 3) + (1 if label_high_potential else 0)
    level = LEVELS[min(level_index, len(LEVELS) - 1)]

    return EmployeeProfile(
        employee_id=f"EMP-{seed or 7:03d}-{index:04d}",
        full_name=f"{first_name} {last_name}",
        department=department,
        job_family=job_family,
        level=level,
        location=location,
        tenure_years=tenure_years,
        age=age,
        performance_score=performance_score,
        peer_feedback_score=peer_feedback_score,
        manager_feedback_score=manager_feedback_score,
        collaboration_score=collaboration_score,
        communication_score=communication_score,
        problem_solving_score=problem_solving_score,
        initiative_score=initiative_score,
        adaptability_score=adaptability_score,
        learning_agility_score=learning_agility_score,
        people_influence_score=people_influence_score,
        decision_quality_score=decision_quality_score,
        project_delivery_score=project_delivery_score,
        engagement_score=engagement_score,
        sentiment_summary=summary,
        career_history=career_history,
        manager_notes=manager_notes,
        label_high_potential=label_high_potential,
    )


def generate_synthetic_workforce(size: int = 250, seed: int | None = 7) -> list[EmployeeProfile]:
    return [generate_synthetic_employee(seed=seed, index=index) for index in range(size)]


def workforce_as_dicts(size: int = 250, seed: int | None = 7) -> list[dict[str, object]]:
    return [profile.model_dump() for profile in generate_synthetic_workforce(size=size, seed=seed)]
