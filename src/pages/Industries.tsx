import { useTranslation } from "react-i18next";
import SiteLayout from "@/components/layout/SiteLayout";
import Container from "@/components/ui/Container";
import SectionHeader from "@/components/sections/SectionHeader";
import Button from "@/components/ui/Button";
import Seo from "@/components/seo/Seo";
import { industries } from "@/content/industries";

export default function Industries() {
  const { t } = useTranslation();

  return (
    <SiteLayout>
      <Seo
        pathname="/industries"
        title={t("industriesPage.seoTitle", "Industries")}
        description={t("industriesPage.seoDescription", "Tailored data and AI transformation services aligned to the constraints, controls, and outcomes of your industry.")}
      />
      <Container className="py-16 md:py-20">
        <SectionHeader
          eyebrow={t("industriesPage.eyebrow", "Industries")}
          title={t("industriesPage.title", "Context matters. So do controls.")}
          description={t("industriesPage.description", "We adapt delivery patterns to your operating model, data constraints, and governance requirements—without losing momentum.")}
        />

        <div className="mt-10 grid gap-4 md:grid-cols-3">
          {industries.map((i) => {
            const title = t(`industries.${i.slug}.title`, { defaultValue: i.title });
            const summary = t(`industries.${i.slug}.summary`, { defaultValue: i.summary });
            return (
              <article key={i.slug} className="rounded-3xl border border-border bg-card/40 p-6">
                <h2 className="text-lg font-semibold tracking-tight">{title}</h2>
                <p className="mt-2 text-sm text-muted">{summary}</p>
                <div className="mt-6">
                  <Button to={`/industries/${i.slug}`} variant="secondary">
                    {t("industriesPage.viewDetails", "View details")}
                  </Button>
                </div>
              </article>
            );
          })}
        </div>
      </Container>
    </SiteLayout>
  );
}

