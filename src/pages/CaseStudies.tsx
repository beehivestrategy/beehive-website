import { Link } from "react-router-dom";
import { useTranslation } from "react-i18next";
import SiteLayout from "@/components/layout/SiteLayout";
import Container from "@/components/ui/Container";
import SectionHeader from "@/components/sections/SectionHeader";
import Tag from "@/components/ui/Tag";
import Button from "@/components/ui/Button";
import Seo from "@/components/seo/Seo";
import { caseStudies } from "@/content/caseStudies";

export default function CaseStudies() {
  const { t } = useTranslation();

  return (
    <SiteLayout>
      <Seo
        pathname="/case-studies"
        title={t("nav.caseStudies", "Case Studies")}
        description={t("caseStudiesPage.seoDescription", "Results-driven examples of data, analytics, and AI transformation work. Clear challenges, approach, and measurable outcomes.")}
      />
      <Container className="py-16 md:py-20">
        <SectionHeader
          eyebrow={t("home.proofSection.eyebrow", "Proof")}
          title={t("caseStudiesPage.headerTitle", "Case studies that focus on measurable outcomes")}
          description={t("caseStudiesPage.headerDescription", "Examples of how we structure work around decision-critical metrics, governance, and sustainable delivery patterns.")}
        />

        <div className="mt-14 grid gap-6 md:grid-cols-2">
          {caseStudies.map((c) => {
            const title = t(`caseStudies.${c.slug}.title`, { defaultValue: c.title });
            const summary = t(`caseStudies.${c.slug}.summary`, { defaultValue: c.summary });
            const industry = t(`caseStudies.${c.slug}.industry`, { defaultValue: c.industry });
            const metrics = t(`caseStudies.${c.slug}.metrics`, { returnObjects: true, defaultValue: c.metrics }) as { label: string; value: string }[];

            return (
              <Link
                key={c.slug}
                to={`/case-studies/${c.slug}`}
                className="group border border-border/50 bg-black/40 backdrop-blur-md p-8 transition-colors hover:border-accent hover:bg-black focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-accent relative overflow-hidden"
              >
                <div className="absolute inset-0 bg-gradient-to-tr from-accent/0 to-accent/0 group-hover:from-accent/[0.03] group-hover:to-transparent transition-colors duration-500" />
                <div className="relative z-10 flex flex-wrap items-center gap-3">
                  <Tag className="bg-transparent text-muted border-border/40">{industry}</Tag>
                </div>

                <h2 className="relative z-10 mt-6 font-display text-2xl font-bold tracking-tight text-white group-hover:text-accent transition-colors">{title}</h2>
                <p className="relative z-10 mt-4 text-base text-muted leading-relaxed">{summary}</p>

                <dl className="relative z-10 mt-8 grid grid-cols-2 gap-4 border-t border-border/50 pt-6">
                  {metrics.slice(0, 2).map((m) => (
                    <div key={m.label}>
                      <dt className="text-[10px] font-bold uppercase tracking-widest text-muted">{m.label}</dt>
                      <dd className="mt-2 text-xl font-display font-bold text-accent">{m.value}</dd>
                    </div>
                  ))}
                </dl>
              </Link>
            );
          })}
        </div>
      </Container>
    </SiteLayout>
  );
}

