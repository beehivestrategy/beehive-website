import { ArrowRight, CheckCircle2 } from "lucide-react";
import { Link } from "react-router-dom";
import { motion } from "framer-motion";
import { useTranslation } from "react-i18next";
import SiteLayout from "@/components/layout/SiteLayout";
import Container from "@/components/ui/Container";
import Button from "@/components/ui/Button";
import Tag from "@/components/ui/Tag";
import HeroGraphics from "@/components/visual/HeroGraphics";
import SectionHeader from "@/components/sections/SectionHeader";
import LeadForm from "@/components/forms/LeadForm";
import NewsletterForm from "@/components/forms/NewsletterForm";
import Seo from "@/components/seo/Seo";
import { services } from "@/content/services";
import { caseStudies } from "@/content/caseStudies";
import { insights } from "@/content/insights";

export default function Home() {
  const { t } = useTranslation();
  const featuredInsights = insights.slice(0, 2);
  const featuredCaseStudy = caseStudies[0];

  const outcomes = [
    { label: t("home.outcomes.cadence"), value: t("home.outcomes.cadenceValue") },
    { label: t("home.outcomes.gov"), value: t("home.outcomes.govValue") },
    { label: t("home.outcomes.impact"), value: t("home.outcomes.impactValue") },
  ];

  return (
    <SiteLayout>
      <Seo
        pathname="/"
        title={t("site.tagline")}
        description={t("site.description")}
      />

      <section className="relative overflow-hidden min-h-[90vh] flex items-center">
        <div aria-hidden="true" className="pointer-events-none absolute inset-0">
          <div className="absolute -top-24 left-1/4 h-[600px] w-[600px] rounded-full bg-accent/10 blur-[120px]" />
          <div className="absolute top-1/2 -right-24 h-[600px] w-[600px] rounded-full bg-cta/10 blur-[120px]" />
        </div>

        <Container className="relative grid gap-12 py-20 md:grid-cols-[1.1fr_0.9fr] md:items-center">
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.8, ease: "easeOut" }}
          >
            <div className="flex flex-wrap items-center gap-2">
              <Tag className="bg-accent/10 border-accent/20 text-accent">{t("home.tag1")}</Tag>
              <Tag>{t("home.tag2")}</Tag>
              <Tag>{t("home.tag3")}</Tag>
            </div>

            <h1 className="mt-8 font-display text-4xl leading-[1.03] tracking-tight md:text-6xl lg:text-7xl text-gradient text-balance">
              {t("home.title")}
            </h1>
            <p className="mt-6 max-w-[55ch] text-lg text-muted md:text-xl leading-relaxed text-pretty">
              {t("home.subtitle")}
            </p>

            <div className="mt-10 flex flex-col gap-4 sm:flex-row sm:items-center">
              <Button to="/contact" variant="primary" size="lg" className="button-glow">
                {t("home.bookConsult")} <ArrowRight aria-hidden="true" className="h-4 w-4 ml-2" />
              </Button>
              <Button to="/services" variant="secondary" size="lg">
                {t("home.exploreServices")}
              </Button>
            </div>

            <dl className="mt-12 grid gap-4 sm:grid-cols-3">
              {outcomes.map((o, i) => (
                <motion.div 
                  key={o.label} 
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: 0.5 + i * 0.1 }}
                  className="border border-border/60 bg-card/20 backdrop-blur-md p-6"
                >
                  <dt className="text-[10px] font-bold uppercase tracking-widest text-muted">{o.label}</dt>
                  <dd className="mt-3 text-sm font-bold text-primary">{o.value}</dd>
                </motion.div>
              ))}
            </dl>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 1, delay: 0.2 }}
            className="relative"
          >
            <HeroGraphics />
            <div className="absolute -bottom-6 -right-6 grid gap-4 border border-border/80 bg-black/90 p-8 shadow-2xl max-w-xs backdrop-blur-xl">
              <div className="text-[10px] font-bold uppercase tracking-widest text-accent">{t("home.whatYouGet")}</div>
              <ul className="grid gap-4 text-sm text-muted">
                <li className="flex gap-3">
                  <CheckCircle2 aria-hidden="true" className="mt-0.5 h-4 w-4 text-white shrink-0" /> {t("home.whatYouGetItems.item1")}
                </li>
                <li className="flex gap-3">
                  <CheckCircle2 aria-hidden="true" className="mt-0.5 h-4 w-4 text-white shrink-0" /> {t("home.whatYouGetItems.item2")}
                </li>
                <li className="flex gap-3">
                  <CheckCircle2 aria-hidden="true" className="mt-0.5 h-4 w-4 text-white shrink-0" /> {t("home.whatYouGetItems.item3")}
                </li>
              </ul>
            </div>
          </motion.div>
        </Container>
      </section>

      <section className="border-t border-border/70 py-16 md:py-20">
        <Container>
          <SectionHeader
            eyebrow={t("home.servicesSection.eyebrow")}
            title={t("home.servicesSection.title")}
            description={t("home.servicesSection.description")}
          />

          <div className="mt-12 grid gap-6 md:grid-cols-2">
            {services.map((s) => (
              <Link
                key={s.slug}
                to={`/services/${s.slug}`}
                className="group relative border border-border bg-black p-6 md:p-8 transition-[border-color,background-color,transform] duration-300 hover:border-accent focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-accent"
              >
                <div className="absolute inset-0 bg-accent/5 opacity-0 group-hover:opacity-100 transition-opacity" />
                <div className="relative flex items-start justify-between gap-6 z-10">
                  <div>
                    <h3 className="font-display text-2xl font-bold uppercase tracking-tight text-white">{t(`services.${s.slug}.title`)}</h3>
                    <p className="mt-3 text-base text-muted leading-relaxed">{t(`services.${s.slug}.summary`)}</p>
                  </div>
                  <div className="grid h-12 w-12 shrink-0 place-items-center border border-border bg-bg/50 text-muted transition-colors duration-300 group-hover:border-accent group-hover:bg-accent group-hover:text-black">
                    <ArrowRight aria-hidden="true" className="h-5 w-5" />
                  </div>
                </div>

                <div className="mt-8 grid gap-3 relative z-10 border-t border-border/50 pt-6">
                  {s.outcomes.slice(0, 3).map((o, idx) => (
                    <div key={o} className="flex gap-3 text-sm text-muted font-medium">
                      <span className="mt-1.5 h-1.5 w-1.5 shrink-0 bg-accent shadow-[2px_2px_0px_rgba(255,255,255,0.2)]" /> {t(`services.${s.slug}.outcomes.${idx}`)}
                    </div>
                  ))}
                </div>
              </Link>
            ))}
          </div>
        </Container>
      </section>

      <section className="border-t border-border/70 py-16 md:py-20">
        <Container className="grid gap-10 md:grid-cols-[1fr_0.9fr] md:items-start">
          <div>
            <SectionHeader
              eyebrow={t("home.proofSection.eyebrow")}
              title={t("home.proofSection.title")}
              description={t("home.proofSection.description")}
            />

            <div className="mt-12 grid gap-6">
              <div className="border border-border bg-black p-6 md:p-8 relative overflow-hidden">
                <div className="absolute top-0 right-0 w-64 h-64 bg-accent/10 blur-[80px] pointer-events-none" />
                <div className="text-[10px] font-bold uppercase tracking-widest text-accent">{t("home.featuredCaseStudy")}</div>
                <div className="mt-4 flex items-start justify-between gap-6 relative z-10">
                  <div>
                    <div className="font-display text-2xl font-bold tracking-tight text-white">{t(`caseStudies.${featuredCaseStudy.slug}.title`)}</div>
                    <div className="mt-3 text-base text-muted leading-relaxed max-w-[50ch]">{t(`caseStudies.${featuredCaseStudy.slug}.summary`)}</div>
                  </div>
                </div>
                <dl className="mt-8 grid gap-4 sm:grid-cols-3 relative z-10">
                  {featuredCaseStudy.metrics.map((m, idx) => (
                    <div key={m.label} className="border border-border/50 bg-bg/50 p-5 backdrop-blur-sm">
                      <dt className="text-[10px] font-bold uppercase tracking-widest text-muted">{t(`caseStudies.${featuredCaseStudy.slug}.metrics.${idx}.label`)}</dt>
                      <dd className="mt-3 text-2xl font-display font-bold text-accent">{t(`caseStudies.${featuredCaseStudy.slug}.metrics.${idx}.value`)}</dd>
                    </div>
                  ))}
                </dl>
                <div className="mt-8 relative z-10">
                  <Button to="/case-studies" variant="secondary" className="!bg-transparent border-white/20 hover:border-accent">
                    {t("home.viewCaseStudies")}
                  </Button>
                </div>
              </div>

              <NewsletterForm source="home-proof" />
            </div>
          </div>

          <div className="md:pt-2">
            <LeadForm source="home" compact />
          </div>
        </Container>
      </section>

      <section className="border-t border-border/70 py-16 md:py-20">
        <Container>
          <SectionHeader
            eyebrow={t("home.insightsSection.eyebrow")}
            title={t("home.insightsSection.title")}
            description={t("home.insightsSection.description")}
          />

          <div className="mt-12 grid gap-6 md:grid-cols-2">
            {featuredInsights.map((p) => (
              <Link
                key={p.slug}
                to={`/insights/${p.slug}`}
                className="group border border-border bg-card/40 backdrop-blur-md p-6 md:p-8 transition-[border-color,background-color] duration-300 hover:border-accent hover:bg-card focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-accent relative overflow-hidden"
              >
                <div className="absolute inset-0 bg-gradient-to-tr from-accent/0 to-accent/0 group-hover:from-accent/[0.05] group-hover:to-transparent transition-colors" />
                <div className="relative z-10 flex flex-wrap gap-2">
                  {p.topics.slice(0, 2).map((topic, idx) => (
                    <Tag key={topic} className="bg-transparent border-border/50 text-muted">{t(`insights.${p.slug}.topics.${idx}`)}</Tag>
                  ))}
                </div>
                <h3 className="mt-6 font-display text-2xl font-bold tracking-tight text-white group-hover:text-accent transition-colors">{t(`insights.${p.slug}.title`)}</h3>
                <p className="mt-4 text-base text-muted leading-relaxed">{t(`insights.${p.slug}.summary`)}</p>
                <div className="mt-8 flex items-center gap-3 text-[10px] font-bold uppercase tracking-widest text-accent">
                  {t("home.readArticle")} <ArrowRight aria-hidden="true" className="h-4 w-4 transition-transform group-hover:translate-x-1" />
                </div>
              </Link>
            ))}
          </div>

          <div className="mt-12 flex justify-center">
            <Button to="/insights" variant="secondary" className="!bg-transparent border-white/20 hover:border-accent">
              {t("home.browseInsights")}
            </Button>
          </div>
        </Container>
      </section>
    </SiteLayout>
  );
}
