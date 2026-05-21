"use client";

import { useState } from "react";

import {
  CandidateInput,
  AssessmentResult,
  defaultCandidate,
  evaluateCandidate,
} from "@/lib/assessment";

type FieldKey = keyof CandidateInput;

const numberFields: Array<{ key: FieldKey; label: string; min: number; max: number; step?: number }> = [
  { key: "tenureYears", label: "Tenure (years)", min: 0, max: 20, step: 0.1 },
  { key: "performanceScore", label: "Performance", min: 0, max: 100 },
  { key: "peerFeedbackScore", label: "Peer feedback", min: 0, max: 100 },
  { key: "managerFeedbackScore", label: "Manager feedback", min: 0, max: 100 },
  { key: "collaborationScore", label: "Collaboration", min: 0, max: 100 },
  { key: "communicationScore", label: "Communication", min: 0, max: 100 },
  { key: "problemSolvingScore", label: "Problem solving", min: 0, max: 100 },
  { key: "initiativeScore", label: "Initiative", min: 0, max: 100 },
  { key: "adaptabilityScore", label: "Adaptability", min: 0, max: 100 },
  { key: "learningAgilityScore", label: "Learning agility", min: 0, max: 100 },
  { key: "peopleInfluenceScore", label: "People influence", min: 0, max: 100 },
  { key: "decisionQualityScore", label: "Decision quality", min: 0, max: 100 },
  { key: "projectDeliveryScore", label: "Project delivery", min: 0, max: 100 },
  { key: "engagementScore", label: "Engagement", min: 0, max: 100 },
];

const textFields: Array<{ key: FieldKey; label: string }> = [
  { key: "fullName", label: "Full name" },
  { key: "employeeId", label: "Employee ID" },
  { key: "department", label: "Department" },
  { key: "jobFamily", label: "Job family" },
  { key: "level", label: "Level" },
  { key: "location", label: "Location" },
];

function RadarChart({ result }: { result: AssessmentResult }) {
  const size = 280;
  const center = size / 2;
  const radius = 104;
  const points = result.radar.map((axis, index) => {
    const angle = -Math.PI / 2 + (index * (Math.PI * 2)) / result.radar.length;
    const scaled = radius * (axis.value / 100);
    return {
      x: center + Math.cos(angle) * scaled,
      y: center + Math.sin(angle) * scaled,
      label: axis.axis,
    };
  });

  const polygon = points.map((point) => `${point.x},${point.y}`).join(" ");

  return (
    <div className="rounded-[28px] border border-[#d9c9b6] bg-white/80 p-5 shadow-[0_20px_60px_rgba(79,54,35,0.12)]">
      <div className="mb-4 flex items-center justify-between">
        <div>
          <p className="text-xs uppercase tracking-[0.34em] text-[#7a6a5b]">Capability map</p>
          <h3 className="text-lg font-semibold text-[#20160f]">Leadership signals</h3>
        </div>
        <span className="rounded-full bg-[#f2e4d6] px-3 py-1 text-xs font-medium text-[#7d4722]">
          {result.tier}
        </span>
      </div>
      <svg viewBox={`0 0 ${size} ${size}`} className="mx-auto block h-[280px] w-full max-w-[280px]">
        {[0.25, 0.5, 0.75, 1].map((ring) => (
          <polygon
            key={ring}
            points={result.radar
              .map((_, index) => {
                const angle = -Math.PI / 2 + (index * (Math.PI * 2)) / result.radar.length;
                const x = center + Math.cos(angle) * radius * ring;
                const y = center + Math.sin(angle) * radius * ring;
                return `${x},${y}`;
              })
              .join(" ")}
            fill="none"
            stroke="rgba(124,92,64,0.16)"
            strokeWidth="1"
          />
        ))}
        <polygon points={polygon} fill="rgba(156,90,42,0.22)" stroke="#9c5a2a" strokeWidth="2" />
        {points.map((point, index) => (
          <g key={point.label}>
            <circle cx={point.x} cy={point.y} r="4" fill={index % 2 === 0 ? "#9c5a2a" : "#30536b"} />
            <text
              x={point.x}
              y={point.y + (point.y < center ? -10 : 18)}
              textAnchor="middle"
              fontSize="11"
              fill="#4a3e34"
            >
              {point.label}
            </text>
          </g>
        ))}
      </svg>
    </div>
  );
}

function Gauge({ score }: { score: number }) {
  const gradient = `conic-gradient(#9c5a2a 0deg ${(score / 100) * 360}deg, #eadfd1 ${(score / 100) * 360}deg 360deg)`;
  return (
    <div className="rounded-[28px] border border-[#d9c9b6] bg-[#fffaf5]/90 p-6 text-center shadow-[0_20px_60px_rgba(79,54,35,0.12)]">
      <div className="mx-auto flex h-44 w-44 items-center justify-center rounded-full" style={{ background: gradient }}>
        <div className="flex h-32 w-32 flex-col items-center justify-center rounded-full bg-[#fffaf5] shadow-inner">
          <span className="text-4xl font-semibold text-[#20160f]">{score.toFixed(1)}</span>
          <span className="text-xs uppercase tracking-[0.28em] text-[#857265]">Leadership score</span>
        </div>
      </div>
      <div className="mt-4 space-y-1">
        <p className="text-sm font-medium text-[#6c5d50]">Interpretation</p>
        <p className="text-lg font-semibold text-[#20160f]">
          {score >= 88 ? "Future leader" : score >= 74 ? "High-potential contributor" : score >= 58 ? "Ready for broader scope" : "Emerging talent"}
        </p>
      </div>
    </div>
  );
}

function DashboardCard({ title, value, description }: { title: string; value: string; description: string }) {
  return (
    <div className="rounded-3xl border border-[#dbcaba] bg-white/85 p-5 shadow-[0_16px_40px_rgba(79,54,35,0.08)]">
      <p className="text-xs uppercase tracking-[0.24em] text-[#7d6e61]">{title}</p>
      <p className="mt-2 text-2xl font-semibold text-[#20160f]">{value}</p>
      <p className="mt-2 text-sm leading-6 text-[#6e6257]">{description}</p>
    </div>
  );
}

function ContributionBars({ contributions }: { contributions: AssessmentResult["contributions"] }) {
  const span = Math.max(...contributions.map((item) => Math.abs(item.impact)), 1);
  return (
    <div className="space-y-3 rounded-[28px] border border-[#d9c9b6] bg-white/85 p-5 shadow-[0_16px_40px_rgba(79,54,35,0.08)]">
      <div>
        <p className="text-xs uppercase tracking-[0.34em] text-[#7a6a5b]">Feature contributions</p>
        <h3 className="text-lg font-semibold text-[#20160f]">Why the score moved</h3>
      </div>
      {contributions.slice(0, 6).map((item) => {
        const width = Math.max(8, (Math.abs(item.impact) / span) * 100);
        return (
          <div key={item.feature} className="space-y-1">
            <div className="flex items-center justify-between text-sm">
              <span className="text-[#4b4037]">{item.feature.replace(/([A-Z])/g, " $1")}</span>
              <span className={item.impact >= 0 ? "text-[#9c5a2a]" : "text-[#9a372c]"}>{item.impact.toFixed(2)}</span>
            </div>
            <div className="h-2 rounded-full bg-[#f0e5d8]">
              <div
                className={`h-2 rounded-full ${item.impact >= 0 ? "bg-[#9c5a2a]" : "bg-[#9a372c]"}`}
                style={{ width: `${width}%` }}
              />
            </div>
          </div>
        );
      })}
    </div>
  );
}

export function AssessmentDashboard() {
  const [candidate, setCandidate] = useState<CandidateInput>(defaultCandidate);
  const [result, setResult] = useState<AssessmentResult>(() => evaluateCandidate(defaultCandidate));

  const updateField = (key: FieldKey, value: string | number) => {
    setCandidate((current) => ({
      ...current,
      [key]: typeof current[key] === "number" ? Number(value) : value,
    }));
  };

  const assess = () => {
    setResult(evaluateCandidate(candidate));
  };

  const reset = () => {
    setCandidate(defaultCandidate);
    setResult(evaluateCandidate(defaultCandidate));
  };

  return (
    <main className="relative min-h-screen overflow-hidden px-4 py-6 sm:px-6 lg:px-8">
      <div className="pointer-events-none absolute inset-0 grid-overlay opacity-35" />
      <div className="mx-auto max-w-7xl">
        <section className="glass-panel relative overflow-hidden rounded-[36px] px-6 py-8 sm:px-8 lg:px-10">
          <div className="absolute inset-x-0 top-0 h-1 bg-gradient-to-r from-[#9c5a2a] via-[#d9a15a] to-[#30536b]" />
          <div className="grid gap-8 lg:grid-cols-[1.1fr_0.9fr]">
            <div className="space-y-6">
              <div className="max-w-3xl space-y-4">
                <p className="inline-flex items-center rounded-full border border-[#d7c2ad] bg-white/60 px-4 py-2 text-xs font-medium uppercase tracking-[0.34em] text-[#7a6a5b]">
                  Leadership potential intelligence
                </p>
                <h1 className="max-w-3xl text-4xl font-semibold leading-tight text-[#1d160f] sm:text-5xl">
                  Assess leadership potential with explainable, agentic scoring.
                </h1>
                <p className="max-w-2xl text-base leading-8 text-[#64584d]">
                  Enter employee or candidate details, score leadership readiness, inspect the decision trace,
                  and review targeted growth recommendations from a modern analytics workflow.
                </p>
              </div>

              <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
                <DashboardCard
                  title="Score band"
                  value={result.tier}
                  description="A normalized assessment tier derived from weighted leadership signals."
                />
                <DashboardCard
                  title="Confidence"
                  value={`${Math.round(result.confidence * 100)}%`}
                  description="Blend of completeness, signal agreement, and trace consistency."
                />
                <DashboardCard
                  title="Decision trace"
                  value={`${result.trace.length} steps`}
                  description="A compact but auditable sequence of reasoning nodes."
                />
                <DashboardCard
                  title="Growth focus"
                  value={`${result.recommendations.length}`}
                  description="Actionable development recommendations for the next review cycle."
                />
              </div>
            </div>

            <div className="grid gap-5">
              <Gauge score={result.score} />
              <div className="rounded-[28px] border border-[#d9c9b6] bg-white/80 p-5 shadow-[0_16px_40px_rgba(79,54,35,0.08)]">
                <p className="text-xs uppercase tracking-[0.34em] text-[#7a6a5b]">Explanation</p>
                <p className="mt-2 text-base leading-8 text-[#3f362e]">{result.explanation}</p>
              </div>
            </div>
          </div>
        </section>

        <section className="mt-6 grid gap-6 xl:grid-cols-[1fr_1fr]">
          <div className="glass-panel rounded-[36px] p-6">
            <div className="flex items-center justify-between gap-4">
              <div>
                <p className="text-xs uppercase tracking-[0.34em] text-[#7a6a5b]">Candidate profile</p>
                <h2 className="text-2xl font-semibold text-[#20160f]">Editable employee details</h2>
              </div>
              <div className="flex gap-3">
                <button
                  type="button"
                  onClick={assess}
                  className="rounded-full bg-[#9c5a2a] px-5 py-3 text-sm font-medium text-white transition hover:bg-[#81431d]"
                >
                  Assess profile
                </button>
                <button
                  type="button"
                  onClick={reset}
                  className="rounded-full border border-[#ccb9a6] bg-white/70 px-5 py-3 text-sm font-medium text-[#4b4037] transition hover:bg-white"
                >
                  Reset
                </button>
              </div>
            </div>

            <form
              className="mt-6 grid gap-4 sm:grid-cols-2"
              onSubmit={(event) => {
                event.preventDefault();
                assess();
              }}
            >
              {textFields.map((field) => (
                <label key={field.key} className="space-y-2 text-sm font-medium text-[#514539]">
                  <span>{field.label}</span>
                  <input
                    value={String(candidate[field.key])}
                    onChange={(event) => updateField(field.key, event.target.value)}
                    className="w-full rounded-2xl border border-[#dbcaba] bg-white/90 px-4 py-3 text-[#221912] outline-none transition focus:border-[#9c5a2a]"
                  />
                </label>
              ))}

              {numberFields.map((field) => (
                <label key={field.key} className="space-y-2 text-sm font-medium text-[#514539]">
                  <div className="flex items-center justify-between gap-3">
                    <span>{field.label}</span>
                    <span className="text-xs text-[#856f5f]">{String(candidate[field.key])}</span>
                  </div>
                  <input
                    type="range"
                    min={field.min}
                    max={field.max}
                    step={field.step ?? 1}
                    value={String(candidate[field.key])}
                    onChange={(event) => updateField(field.key, event.target.value)}
                    className="w-full accent-[#9c5a2a]"
                  />
                </label>
              ))}

              <label className="sm:col-span-2 space-y-2 text-sm font-medium text-[#514539]">
                <span>Sentiment summary</span>
                <textarea
                  rows={4}
                  value={candidate.sentimentSummary}
                  onChange={(event) => updateField("sentimentSummary", event.target.value)}
                  className="w-full rounded-2xl border border-[#dbcaba] bg-white/90 px-4 py-3 text-[#221912] outline-none transition focus:border-[#9c5a2a]"
                />
              </label>

              <label className="sm:col-span-2 space-y-2 text-sm font-medium text-[#514539]">
                <span>Manager notes</span>
                <textarea
                  rows={4}
                  value={candidate.managerNotes}
                  onChange={(event) => updateField("managerNotes", event.target.value)}
                  className="w-full rounded-2xl border border-[#dbcaba] bg-white/90 px-4 py-3 text-[#221912] outline-none transition focus:border-[#9c5a2a]"
                />
              </label>

              <label className="sm:col-span-2 space-y-2 text-sm font-medium text-[#514539]">
                <span>Career history</span>
                <textarea
                  rows={4}
                  value={candidate.careerHistory}
                  onChange={(event) => updateField("careerHistory", event.target.value)}
                  className="w-full rounded-2xl border border-[#dbcaba] bg-white/90 px-4 py-3 text-[#221912] outline-none transition focus:border-[#9c5a2a]"
                />
              </label>
            </form>
          </div>

          <div className="space-y-6">
            <RadarChart result={result} />
            <ContributionBars contributions={result.contributions} />
            <div className="rounded-[28px] border border-[#d9c9b6] bg-white/85 p-5 shadow-[0_16px_40px_rgba(79,54,35,0.08)]">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-xs uppercase tracking-[0.34em] text-[#7a6a5b]">Decision trace</p>
                  <h3 className="text-lg font-semibold text-[#20160f]">How the assessment was built</h3>
                </div>
                <span className="rounded-full bg-[#eff4f7] px-3 py-1 text-xs font-medium text-[#30536b]">
                  {result.trace.length} nodes
                </span>
              </div>
              <div className="mt-4 space-y-3">
                {result.trace.map((step, index) => (
                  <div key={`${step.node}-${index}`} className="rounded-2xl border border-[#e3d3c3] bg-[#fffaf5] px-4 py-3">
                    <p className="text-sm font-semibold text-[#9c5a2a]">{step.node}</p>
                    <p className="mt-1 text-sm leading-6 text-[#514539]">{step.summary}</p>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </section>

        <section className="mt-6 grid gap-6 lg:grid-cols-3">
          <div className="glass-panel rounded-[32px] p-6 lg:col-span-2">
            <div className="flex items-center justify-between gap-3">
              <div>
                <p className="text-xs uppercase tracking-[0.34em] text-[#7a6a5b]">Recommendations</p>
                <h2 className="text-2xl font-semibold text-[#20160f]">Growth actions for the next cycle</h2>
              </div>
              <span className="rounded-full border border-[#d8c3af] bg-white/70 px-3 py-1 text-xs font-medium text-[#6f5f50]">
                AI-generated
              </span>
            </div>
            <div className="mt-5 grid gap-4 md:grid-cols-3">
              {result.recommendations.map((item) => (
                <div key={item} className="rounded-3xl bg-[#fffaf5] p-4 shadow-[0_12px_34px_rgba(79,54,35,0.08)]">
                  <div className="mb-3 h-2 w-16 rounded-full bg-gradient-to-r from-[#9c5a2a] to-[#30536b]" />
                  <p className="text-sm leading-7 text-[#3f362e]">{item}</p>
                </div>
              ))}
            </div>
          </div>

          <div className="glass-panel rounded-[32px] p-6">
            <p className="text-xs uppercase tracking-[0.34em] text-[#7a6a5b]">Strengths & gaps</p>
            <div className="mt-4 space-y-4">
              <div>
                <h3 className="text-sm font-semibold text-[#9c5a2a]">Strengths</h3>
                <ul className="mt-2 space-y-2 text-sm leading-6 text-[#4b4037]">
                  {result.strengths.map((item) => (
                    <li key={item}>• {item}</li>
                  ))}
                </ul>
              </div>
              <div>
                <h3 className="text-sm font-semibold text-[#9a372c]">Weaknesses</h3>
                <ul className="mt-2 space-y-2 text-sm leading-6 text-[#4b4037]">
                  {result.weaknesses.map((item) => (
                    <li key={item}>• {item}</li>
                  ))}
                </ul>
              </div>
            </div>
          </div>
        </section>
      </div>
    </main>
  );
}
