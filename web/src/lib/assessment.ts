export type CandidateInput = {
  employeeId: string;
  fullName: string;
  department: string;
  jobFamily: string;
  level: string;
  location: string;
  tenureYears: number;
  performanceScore: number;
  peerFeedbackScore: number;
  managerFeedbackScore: number;
  collaborationScore: number;
  communicationScore: number;
  problemSolvingScore: number;
  initiativeScore: number;
  adaptabilityScore: number;
  learningAgilityScore: number;
  peopleInfluenceScore: number;
  decisionQualityScore: number;
  projectDeliveryScore: number;
  engagementScore: number;
  sentimentSummary: string;
  managerNotes: string;
  careerHistory: string;
};

export type TraceStep = {
  node: string;
  summary: string;
};

export type Contribution = {
  feature: string;
  value: number;
  impact: number;
};

export type AssessmentResult = {
  score: number;
  tier: string;
  confidence: number;
  strengths: string[];
  weaknesses: string[];
  recommendations: string[];
  explanation: string;
  trace: TraceStep[];
  contributions: Contribution[];
  signals: Record<string, number>;
  radar: { axis: string; value: number }[];
  reportMarkdown: string;
};

const clamp = (value: number, lower = 0, upper = 100) => Math.max(lower, Math.min(upper, value));

export const defaultCandidate: CandidateInput = {
  employeeId: "EMP-241-0001",
  fullName: "Aarav Sharma",
  department: "Engineering",
  jobFamily: "Technical",
  level: "IC4",
  location: "Hybrid",
  tenureYears: 4.7,
  performanceScore: 82,
  peerFeedbackScore: 78,
  managerFeedbackScore: 85,
  collaborationScore: 80,
  communicationScore: 76,
  problemSolvingScore: 84,
  initiativeScore: 88,
  adaptabilityScore: 79,
  learningAgilityScore: 86,
  peopleInfluenceScore: 73,
  decisionQualityScore: 81,
  projectDeliveryScore: 84,
  engagementScore: 77,
  sentimentSummary: "Consistently demonstrates strong ownership, collaborative communication, and growing influence.",
  managerNotes: "Trusted in fast-paced cross-functional work and often takes the lead on ambiguous problems.",
  careerHistory: "Promoted once after leading a key delivery initiative and mentoring junior teammates.",
};

const positiveKeywords = ["ownership", "collaborative", "lead", "trusted", "growth", "mentor", "strategic"];
const negativeKeywords = ["delay", "risk", "unclear", "conflict", "missed", "issue"];

const keywordSignal = (text: string) => {
  const lower = text.toLowerCase();
  const positive = positiveKeywords.reduce((count, word) => count + (lower.includes(word) ? 1 : 0), 0);
  const negative = negativeKeywords.reduce((count, word) => count + (lower.includes(word) ? 1 : 0), 0);
  return clamp(50 + positive * 7 - negative * 8);
};

const tierForScore = (score: number) => {
  if (score >= 88) return "Future Leader";
  if (score >= 74) return "High Potential";
  if (score >= 58) return "Ready Now";
  return "Emerging Talent";
};

export const evaluateCandidate = (candidate: CandidateInput): AssessmentResult => {
  const textSignal = keywordSignal(`${candidate.sentimentSummary} ${candidate.managerNotes} ${candidate.careerHistory}`);
  const execution = clamp(
    candidate.performanceScore * 0.34 + candidate.projectDeliveryScore * 0.33 + candidate.decisionQualityScore * 0.33,
  );
  const influence = clamp(
    candidate.peopleInfluenceScore * 0.4 + candidate.managerFeedbackScore * 0.3 + candidate.peerFeedbackScore * 0.3,
  );
  const growth = clamp(
    candidate.learningAgilityScore * 0.37 + candidate.adaptabilityScore * 0.33 + candidate.initiativeScore * 0.3,
  );
  const team = clamp(candidate.collaborationScore * 0.36 + candidate.communicationScore * 0.28 + candidate.peopleInfluenceScore * 0.36);

  const signals = {
    execution,
    influence,
    growth,
    team,
    text: textSignal,
  };

  const weights: Record<string, number> = {
    performanceScore: 0.12,
    managerFeedbackScore: 0.12,
    initiativeScore: 0.1,
    peopleInfluenceScore: 0.11,
    learningAgilityScore: 0.1,
    collaborationScore: 0.09,
    communicationScore: 0.08,
    decisionQualityScore: 0.08,
    projectDeliveryScore: 0.08,
    adaptabilityScore: 0.07,
    peerFeedbackScore: 0.05,
    engagementScore: 0.03,
  };

  const numericSignals: Record<string, number> = {
    performanceScore: candidate.performanceScore,
    managerFeedbackScore: candidate.managerFeedbackScore,
    initiativeScore: candidate.initiativeScore,
    peopleInfluenceScore: candidate.peopleInfluenceScore,
    learningAgilityScore: candidate.learningAgilityScore,
    collaborationScore: candidate.collaborationScore,
    communicationScore: candidate.communicationScore,
    decisionQualityScore: candidate.decisionQualityScore,
    projectDeliveryScore: candidate.projectDeliveryScore,
    adaptabilityScore: candidate.adaptabilityScore,
    peerFeedbackScore: candidate.peerFeedbackScore,
    engagementScore: candidate.engagementScore,
  };

  const contributions = Object.entries(weights)
    .map(([feature, weight]) => {
      const value = numericSignals[feature];
      const impact = ((value / 100 - 0.5) * weight * 100) + 0.16;
      return { feature, value, impact: Number(impact.toFixed(3)) };
    })
    .sort((left, right) => Math.abs(right.impact) - Math.abs(left.impact));

  const score = clamp(
    (Object.entries(weights).reduce((sum, [feature, weight]) => sum + (numericSignals[feature] / 100) * weight, 0) +
      0.05 * Math.tanh((growth - 55) / 16) +
      0.05 * Math.tanh((team - 55) / 16) +
      0.04 * Math.tanh((influence - 55) / 16) +
      0.16) *
      100,
  );

  const tier = tierForScore(score);
  const confidence = clamp(46 + (growth + team + influence) / 6, 40, 97) / 100;
  const strengths = contributions.filter((item) => item.impact > 0).slice(0, 3).map((item) => `${item.feature.replace(/([A-Z])/g, " $1")} is positive`);
  const weaknesses = contributions.filter((item) => item.impact < 0).slice(-3).map((item) => `${item.feature.replace(/([A-Z])/g, " $1")} needs attention`);

  const recommendations = [
    "Assign a cross-functional initiative with visible business impact.",
    "Provide stretch leadership opportunities that require coaching and stakeholder management.",
    "Pair with a senior sponsor to widen strategic exposure and executive presence.",
  ];

  if (growth > 72) {
    recommendations[1] = "Turn strong learning agility into leadership evidence through a stretch assignment.";
  }
  if (influence < 54) {
    recommendations[2] = "Increase stakeholder-facing work to sharpen influence and executive communication.";
  }

  const trace: TraceStep[] = [
    { node: "ingest", summary: "Canonicalized the employee profile and checked data completeness." },
    { node: "features", summary: "Derived execution, influence, growth, team, and text signals." },
    { node: "scoring", summary: "Computed the weighted leadership score and contribution breakdown." },
    { node: "explainability", summary: "Built a natural language explanation and recommendations." },
    { node: "reporting", summary: "Packaged a dashboard-ready result for the UI and API." },
  ];

  const explanation = `${candidate.fullName} shows a ${tier.toLowerCase()} profile with execution at ${execution.toFixed(
    1,
  )}, influence at ${influence.toFixed(1)}, and growth at ${growth.toFixed(1)}.`;

  const radar = [
    { axis: "Execution", value: execution },
    { axis: "Influence", value: influence },
    { axis: "Growth", value: growth },
    { axis: "Team", value: team },
    { axis: "Text", value: textSignal },
  ];

  const reportMarkdown = `# Leadership Assessment Report\n\n- Candidate: ${candidate.fullName}\n- Tier: ${tier}\n- Score: ${score.toFixed(1)}\n- Confidence: ${(confidence * 100).toFixed(1)}%`;

  return {
    score: Number(score.toFixed(1)),
    tier,
    confidence: Number(confidence.toFixed(3)),
    strengths: strengths.length ? strengths : ["Core indicators are balanced"],
    weaknesses: weaknesses.length ? weaknesses : ["No major gaps were detected"],
    recommendations,
    explanation,
    trace,
    contributions,
    signals,
    radar,
    reportMarkdown,
  };
};
