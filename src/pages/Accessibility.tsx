import SiteLayout from "@/components/layout/SiteLayout";
import Container from "@/components/ui/Container";
import SectionHeader from "@/components/sections/SectionHeader";
import Seo from "@/components/seo/Seo";
import { useTranslation } from "react-i18next";

export default function Accessibility() {
  const { t } = useTranslation();

  return (
    <SiteLayout>
      <Seo
        pathname="/accessibility"
        title={t("accessibilityPage.seoTitle")}
        description={t("accessibilityPage.seoDescription")}
      />
      <Container className="py-16 md:py-20">
        <SectionHeader
          eyebrow={t("accessibilityPage.eyebrow")}
          title={t("accessibilityPage.title")}
          description={t("accessibilityPage.description")}
        />

        <div className="mt-10 grid gap-6 rounded-3xl border border-border bg-card/40 p-6 text-sm text-muted">
          <section>
            <h2 className="text-base font-semibold text-fg">{t("accessibilityPage.commitmentTitle")}</h2>
            <p className="mt-2">{t("accessibilityPage.commitmentContent")}</p>
          </section>
          <section>
            <h2 className="text-base font-semibold text-fg">{t("accessibilityPage.measuresTitle")}</h2>
            <ul className="mt-2 list-disc pl-5">
              {(t("accessibilityPage.measuresList", { returnObjects: true }) as string[]).map((measure, index) => (
                <li key={index}>{measure}</li>
              ))}
            </ul>
          </section>
          <section>
            <h2 className="text-base font-semibold text-fg">{t("accessibilityPage.feedbackTitle")}</h2>
            <p className="mt-2">{t("accessibilityPage.feedbackContent")}</p>
          </section>
        </div>
      </Container>
    </SiteLayout>
  );
}

