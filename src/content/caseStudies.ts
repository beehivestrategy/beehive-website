export type CaseStudy = {
  slug: string;
  title: string;
  industry: string;
  summary: string;
  metrics: { label: string; value: string }[];
  sections: { title: string; body: string[] }[];
  relatedServices: string[];
};

export const caseStudies: CaseStudy[] = [
  {
    slug: "metrics-governance-at-scale",
    title: "Metric Governance for a Multi-Brand Retail Group",
    industry: "Retail & E-commerce",
    summary:
      "Standardized KPI definitions, reduced dashboard drift, and enabled self-serve analytics with clear ownership and change control.",
    metrics: [
      { label: "Dashboard rework", value: "↓ 40%" },
      { label: "Time-to-answer", value: "↓ 30%" },
      { label: "Metric consistency", value: "↑ across teams" },
    ],
    sections: [
      {
        title: "Challenge",
        body: [
          "Multiple business units defined KPIs differently, creating contradictions and undermining trust.",
          "Analysts were overloaded with “why does this number differ?” investigations and manual reconciliation.",
        ],
      },
      {
        title: "Approach",
        body: [
          "Created a KPI hierarchy and a metric dictionary with owners, definitions, and change governance.",
          "Introduced reusable analytics patterns, curated datasets, and templates aligned to decision workflows.",
        ],
      },
      {
        title: "Outcome",
        body: [
          "Improved trust through consistent definitions and transparent ownership.",
          "Enabled faster decision cycles with self-serve patterns and reduced rework.",
        ],
      },
    ],
    relatedServices: ["analytics", "transformation"],
  },
  {
    slug: "ai-productionization-guardrails",
    title: "Operationalizing AI with Evaluation and Governance Guardrails",
    industry: "Financial Services",
    summary:
      "Moved AI capabilities from pilot to production by implementing evaluation, monitoring, and governance patterns aligned to risk and compliance.",
    metrics: [
      { label: "Pilot-to-prod cycle", value: "↓ 35%" },
      { label: "Operational incidents", value: "↓ with guardrails" },
      { label: "Audit readiness", value: "↑ via traceability" },
    ],
    sections: [
      {
        title: "Challenge",
        body: [
          "Promising AI pilots could not pass governance gates due to unclear evaluation, controls, and ownership.",
          "Teams lacked a repeatable pattern for deploying and monitoring AI features responsibly.",
        ],
      },
      {
        title: "Approach",
        body: [
          "Built an evaluation plan covering quality, bias, drift, and cost, with clear thresholds and sign-offs.",
          "Implemented governance controls for access, data usage, and model lifecycle, integrated into delivery.",
        ],
      },
      {
        title: "Outcome",
        body: [
          "Established a repeatable productionization blueprint that balanced speed and risk management.",
          "Improved auditability and reduced rework during approvals and reviews.",
        ],
      },
    ],
    relatedServices: ["ai-enablement", "data-enablement", "transformation"],
  },
];

export function getCaseStudyBySlug(slug: string): CaseStudy | undefined {
  return caseStudies.find((c) => c.slug === slug);
}

