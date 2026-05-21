from __future__ import annotations

from statistics import mean, pstdev
from typing import Any

from .models import AssessmentResult, EmployeeProfile


def _rankdata(values: list[float]) -> list[float]:
    indexed = sorted(enumerate(values), key=lambda item: item[1])
    ranks = [0.0] * len(values)
    i = 0
    while i < len(indexed):
        j = i
        while j + 1 < len(indexed) and indexed[j + 1][1] == indexed[i][1]:
            j += 1
        rank = (i + j + 2) / 2.0
        for k in range(i, j + 1):
            ranks[indexed[k][0]] = rank
        i = j + 1
    return ranks


def roc_auc_score(y_true: list[int], y_score: list[float]) -> float:
    positives = sum(y_true)
    negatives = len(y_true) - positives
    if positives == 0 or negatives == 0:
        return 0.5
    ranks = _rankdata(y_score)
    positive_rank_sum = sum(rank for rank, label in zip(ranks, y_true) if label == 1)
    auc = (positive_rank_sum - positives * (positives + 1) / 2) / (positives * negatives)
    return round(auc, 4)


def _calibration_gap(y_true: list[int], y_score: list[float]) -> float:
    empirical_rate = mean(y_true)
    predicted_rate = mean(score / 100.0 for score in y_score)
    return round(abs(empirical_rate - predicted_rate), 4)


def _stability_index(results: list[AssessmentResult]) -> float:
    if len(results) < 2:
        return 1.0
    return round(1.0 - min(1.0, pstdev([item.leadership_score for item in results]) / 100.0), 4)


def evaluate_batch(
    profiles: list[EmployeeProfile],
    results: list[AssessmentResult],
) -> dict[str, Any]:
    labels = [1 if profile.label_high_potential else 0 for profile in profiles if profile.label_high_potential is not None]
    scores = [result.leadership_score for result in results[: len(labels)]]
    paired_tier_hits = [1 if result.tier.value in {"High Potential", "Future Leader"} else 0 for result in results[: len(labels)]]

    if labels and scores:
        auc = roc_auc_score(labels, scores)
        calibration_gap = _calibration_gap(labels, scores)
        threshold_accuracy = round(sum(int(label == pred) for label, pred in zip(labels, paired_tier_hits)) / len(labels), 4)
    else:
        auc = 0.5
        calibration_gap = 0.0
        threshold_accuracy = 0.0

    score_values = [result.leadership_score for result in results]
    average_confidence = round(mean([result.confidence for result in results]), 4) if results else 0.0

    return {
        "sample_size": len(results),
        "mean_score": round(mean(score_values), 4) if score_values else 0.0,
        "score_std": round(pstdev(score_values), 4) if len(score_values) > 1 else 0.0,
        "average_confidence": average_confidence,
        "label_auc": auc,
        "calibration_gap": calibration_gap,
        "threshold_accuracy": threshold_accuracy,
        "stability_index": _stability_index(results),
        "positive_rate": round(mean(labels), 4) if labels else 0.0,
        "predicted_high_potential_rate": round(mean(paired_tier_hits), 4) if paired_tier_hits else 0.0,
    }


def validation_checks(profile: EmployeeProfile, result: AssessmentResult) -> dict[str, Any]:
    return {
        "score_in_range": 0 <= result.leadership_score <= 100,
        "confidence_in_range": 0.4 <= result.confidence <= 1.0,
        "trace_length": len(result.decision_trace),
        "has_recommendations": bool(result.recommendations),
        "has_explanations": bool(result.explanation),
        "profile_completeness": round(len([v for v in profile.model_dump().values() if v not in (None, "")]) / len(profile.model_fields), 4),
    }
