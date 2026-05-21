from __future__ import annotations

from typing import Any, TypedDict

from langgraph.graph import END, StateGraph

from .evaluation import evaluate_batch, validation_checks
from .explainability import generate_explanation
from .features import derive_features
from .models import AssessmentResult, AssessmentTraceStep, EmployeeProfile
from .preprocessing import preprocess_employee
from .reporting import build_markdown_report
from .scoring import score_leadership
from .synthetic import generate_synthetic_employee, generate_synthetic_workforce


class AssessmentState(TypedDict, total=False):
    employee: EmployeeProfile | dict[str, Any]
    profile: EmployeeProfile
    validation: dict[str, Any]
    features: dict[str, Any]
    scorecard: dict[str, Any]
    explanation: dict[str, Any]
    trace: list[AssessmentTraceStep]
    result: AssessmentResult
    batch_metrics: dict[str, Any]


def _append_trace(state: AssessmentState, node: str, summary: str, status: str = "info", inputs: dict[str, Any] | None = None, outputs: dict[str, Any] | None = None) -> list[AssessmentTraceStep]:
    trace = list(state.get("trace", []))
    trace.append(
        AssessmentTraceStep(
            node=node,
            status=status,  # type: ignore[arg-type]
            summary=summary,
            inputs=inputs or {},
            outputs=outputs or {},
        )
    )
    return trace


def ingest_node(state: AssessmentState) -> AssessmentState:
    profile, validation = preprocess_employee(state["employee"])
    trace = _append_trace(
        state,
        "ingest",
        "Canonicalized the employee record and checked completeness.",
        outputs={"completeness": validation["completeness"]},
    )
    return {"profile": profile, "validation": validation, "trace": trace}


def feature_node(state: AssessmentState) -> AssessmentState:
    features = derive_features(state["profile"])
    trace = _append_trace(
        state,
        "features",
        "Derived execution, influence, growth, team, and text signals.",
        outputs={"signals": features["leadership_shape"]},
    )
    return {"features": features, "trace": trace}


def score_node(state: AssessmentState) -> AssessmentState:
    scorecard = score_leadership(state["profile"], state["features"], state["validation"])
    trace = _append_trace(
        state,
        "scoring",
        "Computed a weighted leadership score and feature contributions.",
        outputs={"score": scorecard["leadership_score"], "tier": scorecard["tier"].value},
    )
    return {"scorecard": scorecard, "trace": trace}


def explain_node(state: AssessmentState) -> AssessmentState:
    explanation = generate_explanation(
        state["profile"].model_dump(),
        state["scorecard"],
        state["features"],
    )
    trace = _append_trace(
        state,
        "explainability",
        "Built natural-language strengths, gaps, and recommendations.",
        outputs={"recommendations": explanation["recommendations"][:2]},
    )
    return {"explanation": explanation, "trace": trace}


def validate_node(state: AssessmentState) -> AssessmentState:
    result = AssessmentResult(
        employee=state["profile"],
        leadership_score=state["scorecard"]["leadership_score"],
        confidence=state["scorecard"]["confidence"],
        tier=state["scorecard"]["tier"],
        strengths=state["explanation"]["strengths"],
        weaknesses=state["explanation"]["weaknesses"],
        recommendations=state["explanation"]["recommendations"],
        explanation=state["explanation"]["explanation"],
        feature_contributions=state["scorecard"]["feature_contributions"],
        decision_trace=state["trace"],
        validation=state["validation"],
        metrics={"completeness": state["validation"]["completeness"]},
        chart_payload={
            "signals": {
                "execution": state["scorecard"]["signal_breakdown"]["execution"],
                "influence": state["scorecard"]["signal_breakdown"]["influence"],
                "growth": state["scorecard"]["signal_breakdown"]["growth"],
                "team": state["scorecard"]["signal_breakdown"]["team"],
                "text": state["features"]["text_features"]["text_signal"],
            }
        },
    )
    result.report_markdown = build_markdown_report(result)
    checks = validation_checks(result.employee, result)
    trace = _append_trace(
        state,
        "validation",
        "Ran output guardrails and format checks.",
        outputs=checks,
    )
    return {"result": result, "trace": trace}


def report_node(state: AssessmentState) -> AssessmentState:
    result = state["result"]
    result.metrics = {
        "quality_checks": state["validation"],
        "chart_ready": True,
        "trace_length": len(result.decision_trace),
    }
    trace = _append_trace(state, "reporting", "Packaged a dashboard-ready JSON report.")
    result.decision_trace = trace
    result.chart_payload["score"] = result.leadership_score
    result.chart_payload["tier"] = result.tier.value
    return {"result": result, "trace": trace}


def build_assessment_graph():
    graph = StateGraph(AssessmentState)
    graph.add_node("ingest", ingest_node)
    graph.add_node("features", feature_node)
    graph.add_node("scoring", score_node)
    graph.add_node("explainability", explain_node)
    graph.add_node("validation", validate_node)
    graph.add_node("reporting", report_node)
    graph.set_entry_point("ingest")
    graph.add_edge("ingest", "features")
    graph.add_edge("features", "scoring")
    graph.add_edge("scoring", "explainability")
    graph.add_edge("explainability", "validation")
    graph.add_edge("validation", "reporting")
    graph.add_edge("reporting", END)
    return graph.compile()


_GRAPH = build_assessment_graph()


def assess_employee(employee: EmployeeProfile | dict[str, Any]) -> AssessmentResult:
    result_state = _GRAPH.invoke({"employee": employee, "trace": []})
    return result_state["result"]


def benchmark_workforce(size: int = 100, seed: int | None = 7) -> dict[str, Any]:
    workforce = generate_synthetic_workforce(size=size, seed=seed)
    results = [assess_employee(profile) for profile in workforce]
    return evaluate_batch(workforce, results)


def sample_assessment(seed: int | None = 7) -> AssessmentResult:
    return assess_employee(generate_synthetic_employee(seed=seed, index=1))
