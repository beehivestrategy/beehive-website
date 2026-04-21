export type Industry = {
  slug: string;
  title: string;
  summary: string;
  painPoints: string[];
  typicalOutcomes: string[];
};

export const industries: Industry[] = [
  {
    slug: "financial-services",
    title: "Financial Services",
    summary:
      "Modernize risk, reporting, and customer analytics with governed data products and auditable AI practices.",
    painPoints: [
      "Conflicting metrics across risk, finance, and product teams",
      "Regulatory reporting and lineage gaps",
      "AI pilots blocked by access, controls, and model risk governance",
    ],
    typicalOutcomes: [
      "Harmonized KPI definitions and data lineage for critical reports",
      "Reduced reporting cycle time through reliable pipelines",
      "Operational AI governance aligned to model risk requirements",
    ],
  },
  {
    slug: "retail-and-ecommerce",
    title: "Retail & E-commerce",
    summary:
      "Improve personalization, forecasting, and marketing effectiveness with reliable, real-time-ready data and pragmatic AI enablement.",
    painPoints: [
      "Fragmented customer identity and event data",
      "Slow experimentation due to analytics bottlenecks",
      "Forecasting accuracy limited by quality and latency",
    ],
    typicalOutcomes: [
      "Unified customer data foundations with measurable identity coverage",
      "Self-serve experimentation and analytics patterns",
      "Forecasting and inventory signals with improved accuracy and governance",
    ],
  },
  {
    slug: "health-and-life-sciences",
    title: "Health & Life Sciences",
    summary:
      "Secure, compliant analytics and AI enablement with strong governance, privacy controls, and transparent decision support.",
    painPoints: [
      "Strict privacy and data access constraints",
      "Inconsistent data definitions across studies and operations",
      "High risk of model drift and explainability requirements",
    ],
    typicalOutcomes: [
      "Governed data products with documented access controls",
      "Consistent definitions and traceability for critical datasets",
      "Evaluation and monitoring patterns suited for regulated environments",
    ],
  },
];

export function getIndustryBySlug(slug: string): Industry | undefined {
  return industries.find((i) => i.slug === slug);
}

