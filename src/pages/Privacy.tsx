import SiteLayout from "@/components/layout/SiteLayout";
import Container from "@/components/ui/Container";
import SectionHeader from "@/components/sections/SectionHeader";
import Seo from "@/components/seo/Seo";
import { useTranslation } from "react-i18next";

export default function Privacy() {
  const { t } = useTranslation();

  return (
    <SiteLayout>
      <Seo pathname="/privacy" title={t("privacyPage.seoTitle")} description={t("privacyPage.seoDescription")} />
      <Container className="py-16 md:py-20">
        <SectionHeader
          eyebrow={t("privacyPage.eyebrow")}
          title={t("privacyPage.title")}
          description={t("privacyPage.description")}
        />

        <div className="mt-10 grid gap-6 rounded-3xl border border-border bg-card/40 p-6 text-sm text-muted">
          {(t("privacyPage.sections", { returnObjects: true }) as { title: string; content: string }[]).map((section, index) => (
            <section key={index}>
              <h2 className="text-base font-semibold text-fg">{section.title}</h2>
              <p className="mt-2">{section.content}</p>
            </section>
          ))}
        </div>
      </Container>
    </SiteLayout>
  );
}

