import { useMemo } from "react";
import { useParams } from "react-router-dom";
import { useTranslation } from "react-i18next";
import SiteLayout from "@/components/layout/SiteLayout";
import Container from "@/components/ui/Container";
import Button from "@/components/ui/Button";
import SectionHeader from "@/components/sections/SectionHeader";
import Tag from "@/components/ui/Tag";
import Seo from "@/components/seo/Seo";
import DataLattice from "@/components/visual/DataLattice";
import LeadForm from "@/components/forms/LeadForm";
import { getServiceBySlug, services } from "@/content/services";

export default function ServiceDetail() {
  const { slug } = useParams();
  const service = slug ? getServiceBySlug(slug) : undefined;
  const { t } = useTranslation();

  const title = service ? t(`services.${service.slug}.title`, { defaultValue: service.title }) : "";
  const summary = service ? t(`services.${service.slug}.summary`, { defaultValue: service.summary }) : "";
  const outcomes = service ? (t(`services.${service.slug}.outcomes`, { returnObjects: true, defaultValue: service.outcomes }) as string[]) : [];
  const deliverables = service ? (t(`services.${service.slug}.deliverables`, { returnObjects: true, defaultValue: service.deliverables }) as string[]) : [];
  const howItWorks = service ? (t(`services.${service.slug}.howItWorks`, { returnObjects: true, defaultValue: service.howItWorks }) as {title: string, description: string}[]) : [];
  const faqs = service ? (t(`services.${service.slug}.faqs`, { returnObjects: true, defaultValue: service.faqs }) as {question: string, answer: string}[]) : [];

  const jsonLd = useMemo(() => {
    if (!service) return undefined;
    return {
      "@context": "https://schema.org",
      "@type": "Service",
      name: title,
      description: summary,
      serviceType: title,
      areaServed: "Global",
    };
  }, [service, title, summary]);

  if (!service) {
    return (
      <SiteLayout>
        <Seo pathname={`/services/${slug ?? ""}`} title={t("serviceDetail.notFound.seoTitle", "Service not found")} />
        <Container className="py-16 md:py-20">
          <SectionHeader
            eyebrow={t("nav.services", "Services")}
            title={t("serviceDetail.notFound.title", "Service not found")}
            description={t("serviceDetail.notFound.description", "Try another service or get in touch and we’ll route you to the right team.")}
          />
          <div className="mt-8 flex flex-wrap gap-3">
            {services.map((s) => (
              <Button key={s.slug} to={`/services/${s.slug}`} variant="secondary">
                {t(`services.${s.slug}.title`, { defaultValue: s.title })}
              </Button>
            ))}
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
      <Seo pathname={`/services/${service.slug}`} title={title} description={summary} jsonLd={jsonLd} />

      <section className="border-b border-border/70">
        <Container className="grid gap-10 py-16 md:grid-cols-[1.1fr_0.9fr] md:items-start md:py-20">
          <div>
            <div className="flex flex-wrap gap-2">
              <Tag>{t("nav.services", "Services")}</Tag>
              <Tag>{title}</Tag>
            </div>
            <h1 className="mt-6 font-display text-4xl tracking-tight md:text-5xl">{title}</h1>
            <p className="mt-4 max-w-[70ch] text-base text-muted md:text-lg">{summary}</p>

            <div className="mt-8 flex flex-wrap items-center gap-3">
              <Button to="/contact" variant="primary" size="lg">
                {t("home.bookConsult", "Book a consult")}
              </Button>
              <Button to="/services" variant="secondary" size="lg">
                {t("nav.services", "All services")}
              </Button>
            </div>

            <section className="mt-10 rounded-3xl border border-border bg-card/40 p-6">
              <h2 className="text-sm font-semibold tracking-tight text-fg">{t("serviceDetail.headers.definition", "Definition")}</h2>
              <p className="mt-2 text-sm text-muted">
                {t("serviceDetail.headers.definitionDescription", { title, defaultValue: `${title} is the combination of delivery practices, governance, and technical patterns that turn strategic intent into reliable outcomes.` })}
              </p>
            </section>
          </div>

          <div className="grid gap-5">
            <div className="relative aspect-[4/3] w-full overflow-hidden border border-border/50 bg-black">
              <img 
                src="https://coresg-normal.trae.ai/api/ide/v1/text_to_image?prompt=photorealistic%20technology%20consulting%20scene%2C%20enterprise%20data%20platform%20visualization%20with%20subtle%20honeycomb%20structure%2C%20teal%20and%20honey%20yellow%20accent%20lighting%2C%20dark%20premium%20aesthetic%2C%20no%20text%2C%20ultra%20detailed&image_size=landscape_4_3" 
                alt="" 
                width="800"
                height="600"
                loading="lazy"
                className="h-full w-full object-cover opacity-80 grayscale mix-blend-luminosity"
              />
              <div className="absolute inset-0 bg-gradient-to-t from-bg via-bg/20 to-transparent mix-blend-multiply" />
            </div>
            <div className="border border-border/50 bg-card p-8">
              <div className="text-[10px] font-bold uppercase tracking-widest text-muted">{t("serviceDetail.headers.typicalOutcomes", "Typical outcomes")}</div>
              <ul className="mt-5 grid gap-4 text-sm text-muted">
                {outcomes.map((o) => (
                  <li key={o} className="flex gap-3">
                    <span className="mt-1.5 h-1.5 w-1.5 shrink-0 rounded-none bg-accent shadow-[2px_2px_0px_rgba(255,255,255,0.2)]" /> {o}
                  </li>
                ))}
              </ul>
            </div>
          </div>
        </Container>
      </section>

      <Container className="grid gap-10 py-16 md:grid-cols-[1fr_0.9fr] md:items-start md:py-20">
        <div className="grid gap-10">
          <section>
            <SectionHeader
              eyebrow={t("serviceDetail.headers.deliverables", "Deliverables")}
              title={t("serviceDetail.headers.whatWeDeliver", "What we deliver")}
              description={t("serviceDetail.headers.whatWeDeliverDescription", "Clear artifacts and reusable patterns your team can adopt and scale.")}
            />
            <ul className="mt-8 grid gap-3">
              {deliverables.map((d) => (
                <li key={d} className="rounded-3xl border border-border bg-card/40 p-5 text-sm text-muted">
                  {d}
                </li>
              ))}
            </ul>
          </section>

          <section>
            <SectionHeader
              eyebrow={t("serviceDetail.headers.howItWorks", "How it works")}
              title={t("serviceDetail.headers.repeatablePattern", "A repeatable delivery pattern")}
              description={t("serviceDetail.headers.repeatablePatternDescription", "A structured approach designed to balance speed, quality, and governance.")}
            />
            <ol className="mt-8 grid gap-4 md:grid-cols-3">
              {howItWorks.map((step) => (
                <li key={step.title} className="rounded-3xl border border-border bg-card/40 p-6">
                  <div className="text-xs font-semibold uppercase tracking-wider text-muted">{step.title}</div>
                  <div className="mt-3 text-sm text-muted">{step.description}</div>
                </li>
              ))}
            </ol>
          </section>

          {faqs.length ? (
            <section>
              <SectionHeader
                eyebrow={t("serviceDetail.headers.faq", "FAQ")}
                title={t("serviceDetail.headers.shortAnswers", "Short answers to common questions")}
                description={t("serviceDetail.headers.shortAnswersDescription", "Clear, decision-ready responses designed for leadership stakeholders.")}
              />
              <div className="mt-8 grid gap-4">
                {faqs.map((f) => (
                  <details key={f.question} className="group rounded-3xl border border-border bg-card/40 p-6">
                    <summary className="cursor-pointer list-none text-sm font-semibold tracking-tight text-fg">
                      {f.question}
                    </summary>
                    <div className="mt-3 text-sm text-muted">{f.answer}</div>
                  </details>
                ))}
              </div>
            </section>
          ) : null}
        </div>

        <div className="md:pt-2">
          <LeadForm source={`service:${service.slug}`} defaultTopic={service.slug} />
        </div>
      </Container>
    </SiteLayout>
  );
}
