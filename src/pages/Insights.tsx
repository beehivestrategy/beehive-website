import { Link } from "react-router-dom";
import { useTranslation } from "react-i18next";
import SiteLayout from "@/components/layout/SiteLayout";
import Container from "@/components/ui/Container";
import SectionHeader from "@/components/sections/SectionHeader";
import Tag from "@/components/ui/Tag";
import NewsletterForm from "@/components/forms/NewsletterForm";
import Seo from "@/components/seo/Seo";
import { insights } from "@/content/insights";

export default function Insights() {
  const { t } = useTranslation();

  return (
    <SiteLayout>
      <Seo
        pathname="/insights"
        title={t("insightsPage.seoTitle", "Insights")}
        description={t("insightsPage.seoDescription", "Thought leadership on data enablement, analytics operating models, AI governance, and practical transformation patterns.")}
      />
      <Container className="py-16 md:py-20">
        <SectionHeader
          eyebrow={t("insightsPage.eyebrow", "Insights")}
          title={t("insightsPage.title", "Practical patterns for data and AI transformation")}
          description={t("insightsPage.description", "Clear frameworks designed to be used: ownership, governance, delivery cadences, and metrics that leaders can act on.")}
        />

        <div className="mt-14 grid gap-6 md:grid-cols-2 lg:grid-cols-3">
          {insights.map((p) => {
            const title = t(`insights.${p.slug}.title`, { defaultValue: p.title });
            const summary = t(`insights.${p.slug}.summary`, { defaultValue: p.summary });
            const topics = t(`insights.${p.slug}.topics`, { returnObjects: true, defaultValue: p.topics }) as string[];

            return (
              <Link
                key={p.slug}
                to={`/insights/${p.slug}`}
                className="group border border-border/50 bg-black/40 backdrop-blur-md p-8 transition-colors hover:border-accent hover:bg-black focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-accent relative overflow-hidden flex flex-col"
              >
                <div className="absolute inset-0 bg-gradient-to-tr from-accent/0 to-accent/0 group-hover:from-accent/[0.03] group-hover:to-transparent transition-colors duration-500" />
                
                <div className="relative z-10 flex flex-wrap gap-2 mb-6">
                  {topics.slice(0, 2).map((tTopic) => (
                    <Tag key={tTopic} className="bg-transparent text-muted border-border/40">{tTopic}</Tag>
                  ))}
                </div>

                <h2 className="relative z-10 font-display text-2xl font-bold tracking-tight text-white group-hover:text-accent transition-colors">{title}</h2>
                <p className="relative z-10 mt-4 text-base text-muted leading-relaxed flex-1">{summary}</p>
                
                <div className="relative z-10 mt-8 flex items-center justify-between gap-3 text-[10px] font-bold uppercase tracking-widest text-accent border-t border-border/50 pt-6">
                  <span>{t("insightsPage.readArticle", "Read article")} <span className="transition-transform group-hover:translate-x-1 inline-block ml-1">→</span></span>
                  <span className="text-muted/60">{p.readingMinutes} {t("insightsPage.minRead", "min read")}</span>
                </div>
              </Link>
            );
          })}
        </div>

        <div className="mt-20 max-w-xl mx-auto">
          <NewsletterForm source="insights" />
        </div>
      </Container>
    </SiteLayout>
  );
}

