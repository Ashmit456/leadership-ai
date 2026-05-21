from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any, Literal

from pydantic import BaseModel, Field


class AssessmentTier(str, Enum):
    emerging = "Emerging Talent"
    ready = "Ready Now"
    high_potential = "High Potential"
    future_leader = "Future Leader"


class EmployeeProfile(BaseModel):
    employee_id: str
    full_name: str
    department: str
    job_family: str
    level: str
    location: str = "Hybrid"
    tenure_years: float = Field(ge=0)
    age: int | None = Field(default=None, ge=18, le=70)
    performance_score: float = Field(ge=0, le=100)
    peer_feedback_score: float = Field(ge=0, le=100)
    manager_feedback_score: float = Field(ge=0, le=100)
    collaboration_score: float = Field(ge=0, le=100)
    communication_score: float = Field(ge=0, le=100)
    problem_solving_score: float = Field(ge=0, le=100)
    initiative_score: float = Field(ge=0, le=100)
    adaptability_score: float = Field(ge=0, le=100)
    learning_agility_score: float = Field(ge=0, le=100)
    people_influence_score: float = Field(ge=0, le=100)
    decision_quality_score: float = Field(ge=0, le=100)
    project_delivery_score: float = Field(ge=0, le=100)
    engagement_score: float = Field(ge=0, le=100)
    sentiment_summary: str = ""
    career_history: str = ""
    manager_notes: str = ""
    label_high_potential: bool | None = None


class AssessmentTraceStep(BaseModel):
    node: str
    status: Literal["success", "warning", "info"] = "info"
    summary: str
    inputs: dict[str, Any] = Field(default_factory=dict)
    outputs: dict[str, Any] = Field(default_factory=dict)
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class FeatureContribution(BaseModel):
    feature: str
    value: float
    impact: float
    direction: Literal["positive", "negative", "neutral"] = "neutral"


class AssessmentResult(BaseModel):
    employee: EmployeeProfile
    leadership_score: float
    confidence: float
    tier: AssessmentTier
    strengths: list[str]
    weaknesses: list[str]
    recommendations: list[str]
    explanation: str
    feature_contributions: list[FeatureContribution]
    decision_trace: list[AssessmentTraceStep]
    validation: dict[str, Any] = Field(default_factory=dict)
    metrics: dict[str, Any] = Field(default_factory=dict)
    chart_payload: dict[str, Any] = Field(default_factory=dict)
    report_markdown: str = ""
