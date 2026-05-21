from __future__ import annotations

from fastapi import FastAPI

from .models import EmployeeProfile
from .synthetic import generate_synthetic_workforce
from .workflow import assess_employee, benchmark_workforce, sample_assessment

app = FastAPI(title="Leadership AI", version="0.1.0")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/sample")
def sample() -> dict[str, object]:
    return {"assessment": sample_assessment().model_dump()}


@app.get("/synthetic-workforce")
def synthetic_workforce(size: int = 25, seed: int = 7) -> dict[str, object]:
    workforce = generate_synthetic_workforce(size=size, seed=seed)
    return {"employees": [employee.model_dump() for employee in workforce]}


@app.post("/assess")
def assess(employee: EmployeeProfile) -> dict[str, object]:
    result = assess_employee(employee)
    return {"assessment": result.model_dump()}


@app.get("/benchmark")
def benchmark(size: int = 100, seed: int = 7) -> dict[str, object]:
    return benchmark_workforce(size=size, seed=seed)
