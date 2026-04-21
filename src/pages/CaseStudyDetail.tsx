import { useMemo } from "react";
import { useParams } from "react-router-dom";
import { useTranslation } from "react-i18next";
import SiteLayout from "@/components/layout/SiteLayout";
import Container from "@/components/ui/Container";
import SectionHeader from "@/components/sections/SectionHeader";
import Tag from "@/components/ui/Tag";
import Button from "@/components/ui/Button";
import Seo from "@/components/seo/Seo";
import { getCaseStudyBySlug } from "@/content/caseStudies";

export default function CaseStudyDetail() {
  const { slug } = useParams();
  const cs = slug ? getCaseStudyBySlug(slug) : undefined;
  const { t } = useTranslation();

  const title = cs ? t(`caseStudies.${cs.slug}.title`, { defaultValue: cs.title }) : "";
  const summary = cs ? t(`caseStudies.${cs.slug}.summary`, { defaultValue: cs.summary }) : "";
  const industry = cs ? t(`caseStudies.${cs.slug}.industry`, { defaultValue: cs.industry }) : "";
  const metrics = cs ? (t(`caseStudies.${cs.slug}.metrics`, { returnObjects: true, defaultValue: cs.metrics }) as { label: string; value: string }[]) : [];
  const sections = cs ? (t(`caseStudies.${cs.slug}.sections`, { returnObjects: true, defaultValue: cs.sections }) as { title: string; body: string[] }[]) : [];

  const jsonLd = useMemo(() => {
    if (!cs) return undefined;
    return {
      "@context": "https://schema.org",
      "@type": "CreativeWork",
      name: title,
      description: summary,
    };
  }, [cs, title, summary]);

  if (!cs) {
    return (
      <SiteLayout>
        <Seo pathname={`/case-studies/${slug ?? ""}`} title={t("caseStudyDetail.notFound.seoTitle", "Case study not found")} />
        <Container className="py-16 md:py-20">
          <SectionHeader
            eyebrow={t("nav.caseStudies", "Case Studies")}
            title={t("caseStudyDetail.notFound.title", "Case study not found")}
            description={t("caseStudyDetail.notFound.description", "Try another case study, or contact us for a tailored conversation.")}
          />
          <div className="mt-8 flex flex-wrap gap-3">
            <Button to="/case-studies" variant="secondary">
              {t("caseStudyDetail.notFound.allCaseStudies", "All case studies")}
            </Button>
            <Button to="/contact" variant="primary">
              {t("nav.contact", "Contact")}
            </Button>
          </div>
        </Container>
      </SiteLayout>
    );
  }

  return (
    <SiteLayout>
      <Seo pathname={`/case-studies/${cs.slug}`} title={title} description={summary} jsonLd={jsonLd} />
      <Container className="py-16 md:py-20">
        <div className="flex flex-wrap items-center gap-3">
          <Tag className="bg-accent/10 border-accent/20 text-accent">{t("caseStudyDetail.tag", "Case study")}</Tag>
          <Tag className="bg-transparent border-border/50">{industry}</Tag>
        </div>
        <h1 className="mt-8 font-display text-5xl tracking-tight md:text-7xl text-gradient text-balance">{title}</h1>
        <p className="mt-6 max-w-[70ch] text-lg text-muted md:text-xl leading-relaxed text-pretty">{summary}</p>

        <dl className="mt-12 grid gap-6 sm:grid-cols-3">
          {metrics.map((m) => (
            <div key={m.label} className="border border-border/50 bg-black/40 backdrop-blur-md p-8">
              <dt className="text-[10px] font-bold uppercase tracking-widest text-muted">{m.label}</dt>
              <dd className="mt-4 text-3xl font-display font-bold tracking-tight text-accent">{m.value}</dd>
            </div>
          ))}
        </dl>

        <article className="mt-16 grid gap-12">
          {sections.map((s) => (
            <section key={s.title} className="border-t border-border/50 pt-8">
              <h2 className="font-display text-2xl font-bold tracking-tight text-white">{s.title}</h2>
              <div className="mt-6 grid gap-4 text-base text-muted leading-relaxed max-w-[75ch]">
                {s.body.map((p) => (
                  <p key={p}>{p}</p>
                ))}
              </div>
            </section>
          ))}
        </article>

        <section className="mt-20 border border-border/50 bg-accent/5 p-10 md:p-14 relative overflow-hidden">
          <div className="absolute top-0 right-0 w-64 h-64 bg-accent/10 blur-[80px] pointer-events-none" />
          <h2 className="font-display text-3xl tracking-tight md:text-4xl text-white relative z-10">{t("caseStudyDetail.cta.title", "Want results like this?")}</h2>
          <p className="mt-4 max-w-[70ch] text-base text-muted md:text-lg leading-relaxed relative z-10">
            {t("caseStudyDetail.cta.description", "Tell us what outcome matters and what constraints you’re operating under. We’ll propose a clear scope and next step.")}
          </p>
          <div className="mt-8 flex flex-wrap gap-4 relative z-10">
            <Button to="/contact" variant="primary" className="button-glow">
              {t("home.bookConsult", "Book a consult")}
            </Button>
            <Button to="/services" variant="secondary" className="!bg-transparent border-white/20 hover:border-accent">
              {t("home.exploreServices", "Explore services")}
            </Button>
          </div>
        </section>
      </Container>
    </SiteLayout>
  );
}

