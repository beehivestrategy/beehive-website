export type ServiceSlug =
  | "data-enablement"
  | "analytics"
  | "transformation"
  | "ai-enablement";

export type ServiceFaq = { question: string; answer: string };

export type Service = {
  slug: ServiceSlug;
  title: string;
  summary: string;
  outcomes: string[];
  deliverables: string[];
  howItWorks: { title: string; description: string }[];
  faqs: ServiceFaq[];
};

export const services: Service[] = [
  {
    slug: "data-enablement",
    title: "Data Enablement",
    summary:
      "Modern data foundations: architecture, platforms, governance, and delivery practices that make data reliable and usable.",
    outcomes: [
      "Faster time-to-data with dependable pipelines",
      "Trusted definitions and lineage for critical metrics",
      "Reduced operational risk through governance-by-design",
    ],
    deliverables: [
      "Reference architecture and platform blueprint",
      "Ingestion + transformation patterns and standards",
      "Semantic layer / metrics definitions (where applicable)",
      "Governance operating model and controls",
    ],
    howItWorks: [
      {
        title: "Assess",
        description:
          "Rapid discovery to map systems, bottlenecks, and priority domains with measurable outcomes.",
      },
      {
        title: "Design",
        description:
          "Architecture and operating model aligned to security, compliance, and the way teams actually work.",
      },
      {
        title: "Deliver",
        description:
          "Iterative delivery: build high-value pipelines and patterns first, then scale with guardrails.",
      },
    ],
    faqs: [
      {
        question: "Do you replace our existing platform?",
        answer:
          "Only when it’s justified. Most engagements modernize incrementally: improve reliability, observability, governance, and domain delivery while keeping what works.",
      },
      {
        question: "How do you define “trusted data”?",
        answer:
          "Data that is discoverable, documented, lineage-aware, quality-checked, and governed with clear ownership—so decision-makers can act confidently.",
      },
    ],
  },
  {
    slug: "analytics",
    title: "Analytics Enablement",
    summary:
      "From ad-hoc reporting to scalable insight delivery: a semantic layer, metric governance, and an analytics operating rhythm.",
    outcomes: [
      "Metric consistency across teams and tools",
      "Self-serve insights with lower analyst load",
      "Clear accountability for definitions and changes",
    ],
    deliverables: [
      "KPI hierarchy and metric dictionary",
      "Analytics product backlog and operating cadence",
      "Dashboards and narrative reporting patterns",
      "Enablement materials and playbooks",
    ],
    howItWorks: [
      {
        title: "Align",
        description:
          "Define decision-critical KPIs and the questions they must answer across functions.",
      },
      {
        title: "Standardize",
        description:
          "Create metric governance and semantic definitions to prevent drift and contradiction.",
      },
      {
        title: "Scale",
        description:
          "Enable self-serve with curated datasets, templates, and training so teams move faster.",
      },
    ],
    faqs: [
      {
        question: "Can you work with our BI tooling?",
        answer:
          "Yes. We design around business outcomes and governance; tooling follows. We can adapt patterns to common BI and semantic approaches.",
      },
      {
        question: "Will this reduce our reporting backlog?",
        answer:
          "Typically, yes—by clarifying definitions, creating reusable data products, and moving repetitive requests to governed self-serve.",
      },
    ],
  },
  {
    slug: "transformation",
    title: "Data & AI Transformation",
    summary:
      "Operating model, delivery practices, and capability build to sustain change—beyond a single platform initiative.",
    outcomes: [
      "Cross-functional delivery aligned to business value",
      "A pragmatic roadmap with dependencies and governance",
      "Teams enabled to ship and iterate with confidence",
    ],
    deliverables: [
      "Transformation roadmap and initiative sequencing",
      "Operating model (roles, rituals, decision rights)",
      "Portfolio governance and prioritization framework",
      "Capability uplift plan (skills, process, tooling)",
    ],
    howItWorks: [
      {
        title: "Diagnose",
        description:
          "Identify the real constraints: org design, data ownership, process friction, and incentives.",
      },
      {
        title: "Mobilize",
        description:
          "Create a value-backed roadmap with delivery waves, risk controls, and measurable KPIs.",
      },
      {
        title: "Embed",
        description:
          "Support teams during delivery, building repeatable ways of working and governance.",
      },
    ],
    faqs: [
      {
        question: "What makes your approach different?",
        answer:
          "We treat data and AI as products with accountable ownership, quality controls, and delivery cadences—so the change sticks after consultants leave.",
      },
      {
        question: "Do you support governance and risk teams?",
        answer:
          "Yes. We align controls to real delivery workflows and implement guardrails that reduce risk without slowing teams down.",
      },
    ],
  },
  {
    slug: "ai-enablement",
    title: "AI Enablement",
    summary:
      "Operationalize AI safely: use case selection, data readiness, model governance, and productization patterns that move from pilots to value.",
    outcomes: [
      "AI use cases prioritized by feasibility and ROI",
      "Governance for models, prompts, and data access",
      "Repeatable delivery pattern for AI features",
    ],
    deliverables: [
      "Use case portfolio + prioritization scorecard",
      "Data readiness and governance controls",
      "Evaluation plan (quality, bias, drift, cost)",
      "Productionization blueprint and handover",
    ],
    howItWorks: [
      {
        title: "Select",
        description:
          "Choose use cases with measurable outcomes and clear operational ownership.",
      },
      {
        title: "Govern",
        description:
          "Implement policies and controls for access, safety, and responsible use.",
      },
      {
        title: "Ship",
        description:
          "Deliver AI features with evaluation, monitoring, and change management built in.",
      },
    ],
    faqs: [
      {
        question: "Can you help us move beyond pilots?",
        answer:
          "Yes. We focus on the missing pieces: data readiness, evaluation, governance, and ownership so AI capabilities can be sustained in production.",
      },
      {
        question: "Do you support responsible AI requirements?",
        answer:
          "Yes. We incorporate risk, safety, privacy, and auditability into the delivery pattern and operating model.",
      },
    ],
  },
];

export function getServiceBySlug(slug: string): Service | undefined {
  return services.find((s) => s.slug === slug);
}

