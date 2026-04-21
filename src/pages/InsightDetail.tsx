import { useMemo } from "react";
import { useParams } from "react-router-dom";
import { useTranslation } from "react-i18next";
import SiteLayout from "@/components/layout/SiteLayout";
import Container from "@/components/ui/Container";
import SectionHeader from "@/components/sections/SectionHeader";
import Tag from "@/components/ui/Tag";
import Button from "@/components/ui/Button";
import NewsletterForm from "@/components/forms/NewsletterForm";
import Seo from "@/components/seo/Seo";
import TableOfContents from "@/components/insights/TableOfContents";
import { getInsightBySlug } from "@/content/insights";

function toId(heading: string) {
  return heading
    .toLowerCase()
    .replace(/[^\w\s-]/g, "")
    .trim()
    .replace(/\s+/g, "-");
}

export default function InsightDetail() {
  const { slug } = useParams();
  const { t } = useTranslation();
  const post = slug ? getInsightBySlug(slug) : undefined;

  const sections = useMemo(() => {
    if (!post) return [];
    return t(`insights.${post.slug}.sections`, { returnObjects: true, defaultValue: post.sections }) as Array<{heading: string; paragraphs: string[]}>;
  }, [post, t]);

  const toc = useMemo(() => {
    return sections.map((s) => ({ id: toId(s.heading), label: s.heading }));
  }, [sections]);

  const title = post ? t(`insights.${post.slug}.title`, { defaultValue: post.title }) : "";
  const summary = post ? t(`insights.${post.slug}.summary`, { defaultValue: post.summary }) : "";
  const topics = post ? t(`insights.${post.slug}.topics`, { returnObjects: true, defaultValue: post.topics }) as string[] : [];
  const faqs = post ? t(`insights.${post.slug}.faqs`, { returnObjects: true, defaultValue: post.faqs || [] }) as Array<{question: string; answer: string}> : [];

  const jsonLd = useMemo(() => {
    if (!post) return undefined;
    return {
      "@context": "https://schema.org",
      "@type": "Article",
      headline: title,
      datePublished: post.publishedAt,
      description: summary,
      mainEntityOfPage: { "@type": "WebPage", "@id": `/insights/${post.slug}` },
    };
  }, [post, title, summary]);

  const faqJsonLd = useMemo(() => {
    if (!faqs.length) return undefined;
    return {
      "@context": "https://schema.org",
      "@type": "FAQPage",
      mainEntity: faqs.map((f) => ({
        "@type": "Question",
        name: f.question,
        acceptedAnswer: { "@type": "Answer", text: f.answer },
      })),
    };
  }, [faqs]);

  const combinedJsonLd = useMemo(() => {
    if (!jsonLd) return undefined;
    if (!faqJsonLd) return jsonLd;
    return [jsonLd, faqJsonLd];
  }, [jsonLd, faqJsonLd]);

  if (!post) {
    return (
      <SiteLayout>
        <Seo pathname={`/insights/${slug ?? ""}`} title={t("insightsPage.notFoundTitle", "Insight not found")} />
        <Container className="py-16 md:py-20">
          <SectionHeader eyebrow={t("insightsPage.eyebrow", "Insights")} title={t("insightsPage.notFoundTitle", "Insight not found")} description={t("insightsPage.notFoundDescription", "Try another article or browse all insights.")} />
          <div className="mt-8 flex flex-wrap gap-3">
            <Button to="/insights" variant="secondary">
              {t("insightsPage.allInsights", "All insights")}
            </Button>
            <Button to="/contact" variant="primary">
              {t("insightsPage.contact", "Contact")}
            </Button>
          </div>
        </Container>
      </SiteLayout>
    );
  }

  return (
    <SiteLayout>
      <Seo
        pathname={`/insights/${post.slug}`}
        title={title}
        description={summary}
        ogType="article"
        publishedTime={new Date(post.publishedAt).toISOString()}
        jsonLd={combinedJsonLd}
      />
      <Container className="py-16 md:py-20">
        <div className="flex flex-wrap gap-2">
          <Tag className="bg-accent/10 border-accent/20 text-accent">{t("insightsPage.eyebrow", "Insight")}</Tag>
          {topics.slice(0, 3).map((tTopic) => (
            <Tag key={tTopic} className="bg-transparent border-border/50">{tTopic}</Tag>
          ))}
        </div>
        <h1 className="mt-8 font-display text-5xl tracking-tight md:text-7xl text-gradient text-balance">{title}</h1>
        <p className="mt-6 max-w-[74ch] text-lg text-muted md:text-xl leading-relaxed text-pretty">{summary}</p>
        <div className="mt-6 text-xs font-bold uppercase tracking-widest text-muted flex items-center gap-2">
          <span>{post.readingMinutes} {t("insightsPage.minRead", "min read")}</span>
          <span className="text-border">•</span>
          <span>{new Date(post.publishedAt).toLocaleDateString(undefined, { year: "numeric", month: "short", day: "numeric" })}</span>
        </div>

        <div className="mt-16 grid gap-10 md:grid-cols-[1fr_0.8fr] lg:grid-cols-[1fr_0.6fr] md:items-start">
          <article className="grid gap-8">
            {sections.map((s) => {
              const id = toId(s.heading);
              return (
                <section key={id} id={id} className="scroll-mt-32">
                  <h2 className="font-display text-2xl font-bold tracking-tight text-white mb-6">{s.heading}</h2>
                  <div className="grid gap-4 text-base text-muted leading-relaxed">
                    {s.paragraphs.map((p, index) => (
                      <p key={index}>{p}</p>
                    ))}
                  </div>
                </section>
              );
            })}

            {faqs.length ? (
              <section className="mt-12 border-t border-border/50 pt-12">
                <h2 className="font-display text-2xl font-bold tracking-tight text-white mb-8">{t("insightsPage.faq", "FAQ")}</h2>
                <div className="grid gap-4">
                  {faqs.map((f) => (
                    <details key={f.question} className="group border border-border/50 bg-black/40 backdrop-blur-md p-6 [&_summary::-webkit-details-marker]:hidden">
                      <summary className="flex cursor-pointer items-center justify-between text-base font-bold tracking-tight text-white focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-accent rounded-sm">
                        {f.question}
                        <span className="transition duration-300 group-open:rotate-180 ml-4 shrink-0 text-accent">
                          <svg aria-hidden="true" xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="m6 9 6 6 6-6"/></svg>
                        </span>
                      </summary>
                      <div className="mt-4 text-sm text-muted leading-relaxed border-t border-border/50 pt-4">{f.answer}</div>
                    </details>
                  ))}
                </div>
              </section>
            ) : null}
          </article>

          <aside className="grid gap-6 sticky top-24">
            <TableOfContents items={toc} />
            <NewsletterForm source={`insight:${post.slug}`} />
            <div className="border border-border/50 bg-accent/5 p-8 relative overflow-hidden">
              <div className="absolute top-0 right-0 w-32 h-32 bg-accent/10 blur-[40px] pointer-events-none" />
              <div className="text-[10px] font-bold uppercase tracking-widest text-accent">{t("insightsPage.wantHelp", "Want help applying this?")}</div>
              <p className="mt-4 text-sm text-muted leading-relaxed relative z-10">
                {t("insightsPage.wantHelpDescription", "We’ll help you scope a practical next step—diagnostic, roadmap, or delivery sprint.")}
              </p>
              <div className="mt-8 relative z-10">
                <Button to="/contact" variant="primary" className="w-full justify-center button-glow">
                  {t("insightsPage.bookConsult", "Book a consult")}
                </Button>
              </div>
            </div>
          </aside>
        </div>
      </Container>
    </SiteLayout>
  );
}
