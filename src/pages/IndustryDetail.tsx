import { useParams } from "react-router-dom";
import { useTranslation } from "react-i18next";
import SiteLayout from "@/components/layout/SiteLayout";
import Container from "@/components/ui/Container";
import SectionHeader from "@/components/sections/SectionHeader";
import Tag from "@/components/ui/Tag";
import Button from "@/components/ui/Button";
import Seo from "@/components/seo/Seo";
import { getIndustryBySlug } from "@/content/industries";

export default function IndustryDetail() {
  const { slug } = useParams();
  const { t } = useTranslation();
  const industry = slug ? getIndustryBySlug(slug) : undefined;

  if (!industry) {
    return (
      <SiteLayout>
        <Seo pathname={`/industries/${slug ?? ""}`} title={t("industriesPage.notFoundTitle", "Industry not found")} />
        <Container className="py-16 md:py-20">
          <SectionHeader
            eyebrow={t("industriesPage.eyebrow", "Industries")}
            title={t("industriesPage.notFoundTitle", "Industry not found")}
            description={t("industriesPage.notFoundDescription", "Try another industry page, or get in touch and we’ll route you to the right team.")}
          />
          <div className="mt-8 flex flex-wrap gap-3">
            <Button to="/industries" variant="secondary">
              {t("industriesPage.allIndustries", "All industries")}
            </Button>
            <Button to="/contact" variant="primary">
              {t("industriesPage.contact", "Contact")}
            </Button>
          </div>
        </Container>
      </SiteLayout>
    );
  }

  const title = t(`industries.${industry.slug}.title`, { defaultValue: industry.title });
  const summary = t(`industries.${industry.slug}.summary`, { defaultValue: industry.summary });
  const painPoints = t(`industries.${industry.slug}.painPoints`, { returnObjects: true, defaultValue: industry.painPoints }) as string[];
  const typicalOutcomes = t(`industries.${industry.slug}.typicalOutcomes`, { returnObjects: true, defaultValue: industry.typicalOutcomes }) as string[];

  return (
    <SiteLayout>
      <Seo pathname={`/industries/${industry.slug}`} title={title} description={summary} />
      <Container className="py-16 md:py-20">
        <div className="flex flex-wrap gap-2">
          <Tag className="bg-accent/10 border-accent/20 text-accent">{t("industriesPage.eyebrow", "Industries")}</Tag>
          <Tag className="bg-transparent border-border/50">{title}</Tag>
        </div>
        <h1 className="mt-8 font-display text-5xl tracking-tight md:text-7xl text-gradient text-balance">{title}</h1>
        <p className="mt-6 max-w-[70ch] text-lg text-muted md:text-xl leading-relaxed text-pretty">{summary}</p>

        <div className="mt-16 grid gap-8 md:grid-cols-2">
          <section className="border border-border/50 bg-black/40 backdrop-blur-md p-8">
            <div className="text-[10px] font-bold uppercase tracking-widest text-accent">{t("industriesPage.commonConstraints", "Common constraints")}</div>
            <ul className="mt-6 grid gap-4 text-base text-muted leading-relaxed">
              {painPoints.map((p) => (
                <li key={p} className="flex gap-4">
                  <span className="mt-2 h-1.5 w-1.5 shrink-0 bg-cta shadow-[2px_2px_0px_rgba(255,255,255,0.2)]" /> {p}
                </li>
              ))}
            </ul>
          </section>
          <section className="border border-border/50 bg-black/40 backdrop-blur-md p-8">
            <div className="text-[10px] font-bold uppercase tracking-widest text-accent">{t("industriesPage.typicalOutcomes", "Typical outcomes")}</div>
            <ul className="mt-6 grid gap-4 text-base text-muted leading-relaxed">
              {typicalOutcomes.map((o) => (
                <li key={o} className="flex gap-4">
                  <span className="mt-2 h-1.5 w-1.5 shrink-0 bg-accent shadow-[2px_2px_0px_rgba(255,255,255,0.2)]" /> {o}
                </li>
              ))}
            </ul>
          </section>
        </div>

        <section className="mt-16 border border-border/50 bg-accent/5 p-10 md:p-14 relative overflow-hidden">
          <div className="absolute top-0 right-0 w-64 h-64 bg-accent/10 blur-[80px] pointer-events-none" />
          <h2 className="font-display text-3xl tracking-tight md:text-4xl text-white relative z-10">{t("industriesPage.nextSteps", "Next steps")}</h2>
          <p className="mt-4 max-w-[70ch] text-base text-muted md:text-lg leading-relaxed relative z-10">
            {t("industriesPage.nextStepsDescription", "We’ll help you scope the highest-value initiatives, align governance, and deliver a repeatable pattern that works within your constraints.")}
          </p>
          <div className="mt-8 flex flex-wrap gap-4 relative z-10">
            <Button to="/contact" variant="primary" className="button-glow">
              {t("industriesPage.bookConsult", "Book a consult")}
            </Button>
            <Button to="/services" variant="secondary" className="!bg-transparent border-white/20 hover:border-accent">
              {t("industriesPage.exploreServices", "Explore services")}
            </Button>
          </div>
        </section>
      </Container>
    </SiteLayout>
  );
}

