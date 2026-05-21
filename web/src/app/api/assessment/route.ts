import { NextResponse } from "next/server";

import { evaluateCandidate, type CandidateInput, defaultCandidate } from "@/lib/assessment";

export async function GET() {
  return NextResponse.json({ assessment: evaluateCandidate(defaultCandidate) });
}

export async function POST(request: Request) {
  const body = (await request.json()) as Partial<CandidateInput>;
  const candidate = { ...defaultCandidate, ...body } as CandidateInput;
  return NextResponse.json({ assessment: evaluateCandidate(candidate) });
}
