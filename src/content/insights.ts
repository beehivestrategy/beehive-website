export type InsightFaq = { question: string; answer: string };

export type Insight = {
  slug: string;
  title: string;
  summary: string;
  publishedAt: string;
  readingMinutes: number;
  topics: string[];
  sections: { heading: string; paragraphs: string[] }[];
  faqs?: InsightFaq[];
};

export const insights: Insight[] = [
  {
    slug: "building-modern-data-foundations-for-enterprise-ai-success",
    title: "Building Modern Data Foundations for Enterprise AI Success",
    summary: "Enterprises that invest in robust data foundations accelerate AI deployment and achieve measurable business impact. This article outlines the essential pillars, operational practices, and governance frameworks required for sustainable AI at scale.",
    publishedAt: "2026-04-26",
    readingMinutes: 5,
    topics: ["data enablement","ai enablement","strategy"],
    sections: [],
    faqs: []
  },
  {
    slug: "modern-data-foundations-ai-operationalization-strategic-blueprint",
    title: "Modern Data Foundations and AI Operationalization: A Strategic Blueprint for Enterprise Leaders",
    summary: "Enterprises increasingly recognize that robust data foundations are the prerequisite for scaling AI initiatives. This article outlines a pragmatic framework for establishing governed, metric-driven data pipelines and operationalizing AI to deliver measurable business value.",
    publishedAt: "2026-04-25",
    readingMinutes: 5,
    topics: ["data enablement","ai enablement","strategy"],
    sections: [],
    faqs: []
  },
  {
    slug: "modern-data-foundations-and-ai-operationalization-beyond-the-hype",
    title: "Modern Data Foundations & AI Operationalization: Beyond the Hype",
    summary: "This article dissects the critical intersection of robust data foundations and AI operationalization, revealing how enterprises can transition from theoretical capabilities to measurable, business-impactful outcomes. Key insights include the role of centralized data governance, real-time data mesh architectures, and the alignment of AI models with operational KPIs to drive enterprise agility.",
    publishedAt: "2026-04-24",
    readingMinutes: 5,
    topics: ["data enablement","ai enablement","strategy"],
    sections: [],
    faqs: []
  },
  {
    slug: "modern-data-foundations-and-ai-operationalization",
    title: "Modern Data Foundations and AI Operationalization",
    summary: "Enterprises must align robust data foundations with scalable AI operationalization to unlock sustainable value. This article outlines the strategic pillars required to integrate data integrity with intelligent automation.",
    publishedAt: "2026-04-24",
    readingMinutes: 5,
    topics: ["data enablement","ai enablement","strategy"],
    sections: [],
    faqs: []
  },
  {
    slug: "data-products-operating-model",
    title: "Data Products: The Operating Model That Makes Data Useful",
    summary:
      "Data products turn pipelines into outcomes by creating accountable ownership, quality controls, and a delivery cadence built around consumers.",
    publishedAt: "2026-03-10",
    readingMinutes: 7,
    topics: ["data enablement", "governance", "operating model"],
    sections: [
      {
        heading: "What a data product is (and isn’t)",
        paragraphs: [
          "A data product is a reusable, governed data asset designed for a defined consumer group. It has an owner, service-level expectations, documentation, and a lifecycle.",
          "It isn’t “a dataset somewhere.” It isn’t a dashboard. It’s an owned capability that teams rely on to make decisions and build features.",
        ],
      },
      {
        heading: "Why traditional data delivery breaks at scale",
        paragraphs: [
          "When ownership is unclear, quality issues become everyone’s problem and nobody’s responsibility. Definitions drift, pipelines become fragile, and trust collapses.",
          "Data products are a practical answer because they define who owns what, how quality is measured, and how change is governed.",
        ],
      },
      {
        heading: "The minimum viable operating model",
        paragraphs: [
          "Start with three ingredients: accountable owners, measurable quality, and a visible backlog. Add lightweight governance that fits delivery workflows rather than creating parallel bureaucracy.",
          "The goal is not compliance theatre—it’s reliable delivery with transparent risk controls.",
        ],
      },
    ],
    faqs: [
      {
        question: "Do we need a full data mesh to start?",
        answer:
          "No. Many organizations benefit from product thinking without adopting every concept. Start with ownership and quality, then evolve architecture and domains as the organization matures.",
      },
      {
        question: "Who should own a data product?",
        answer:
          "The owner should be accountable for outcomes and have decision authority over definition, access, and change management—often a product-aligned data lead partnered with domain stakeholders.",
      },
    ],
  },
  {
    slug: "ai-governance-that-enables-delivery",
    title: "AI Governance That Enables Delivery (Not Just Approvals)",
    summary:
      "Responsible AI is a delivery pattern. Teams move faster when evaluation, monitoring, and controls are built into the workflow from day one.",
    publishedAt: "2026-02-18",
    readingMinutes: 6,
    topics: ["ai enablement", "risk", "governance"],
    sections: [
      {
        heading: "Treat governance as a system, not a committee",
        paragraphs: [
          "Approval-only governance creates bottlenecks and rework. Delivery-first governance defines controls teams can apply continuously: access rules, evaluation thresholds, and monitoring expectations.",
          "The best governance makes safe delivery the default rather than a special case.",
        ],
      },
      {
        heading: "Evaluation as the new unit of quality",
        paragraphs: [
          "For AI features, quality is not just accuracy. You need measurable expectations across reliability, bias, cost, and drift—plus an owner who responds when reality changes.",
          "Evaluation becomes the contract between delivery teams and risk stakeholders.",
        ],
      },
      {
        heading: "A practical checklist for shipping responsibly",
        paragraphs: [
          "Define use case boundaries, data access, and allowed behaviors. Create test sets and success metrics. Monitor usage and performance. Document decisions for auditability.",
          "This can be lightweight and repeatable. It doesn’t require months of policy writing before shipping value.",
        ],
      },
    ],
  },
  {
    slug: "analytics-metrics-trust",
    title: "Why Metrics Fail: Drift, Definitions, and the Trust Gap",
    summary:
      "Most analytics programs don’t fail on dashboards—they fail on definitions. Metric governance reduces churn and restores decision confidence.",
    publishedAt: "2026-01-25",
    readingMinutes: 5,
    topics: ["analytics", "metrics", "strategy"],
    sections: [
      {
        heading: "The trust gap is expensive",
        paragraphs: [
          "When teams don’t trust numbers, they stop acting. Decisions slow down, reporting debates intensify, and analysts become referees instead of enablers.",
          "The hidden cost is opportunity: fewer experiments, slower execution, and more defensive decision-making.",
        ],
      },
      {
        heading: "How drift happens",
        paragraphs: [
          "Definitions change silently across tools and teams. Small differences accumulate until every dashboard tells a different story.",
          "Drift is not a tooling problem; it’s an ownership and change-control problem.",
        ],
      },
      {
        heading: "What works in practice",
        paragraphs: [
          "Define KPI hierarchies, assign owners, document definitions, and implement lightweight change governance. Prioritize the metrics that drive decisions and revenue.",
          "The result is fewer debates, faster alignment, and analytics that teams actually use.",
        ],
      },
    ],
  },
];

export function getInsightBySlug(slug: string): Insight | undefined {
  return insights.find((p) => p.slug === slug);
}

