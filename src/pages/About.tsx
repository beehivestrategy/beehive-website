import SiteLayout from "@/components/layout/SiteLayout";
import Container from "@/components/ui/Container";
import SectionHeader from "@/components/sections/SectionHeader";
import Tag from "@/components/ui/Tag";
import Button from "@/components/ui/Button";
import Seo from "@/components/seo/Seo";
import { useTranslation } from "react-i18next";

export default function About() {
  const { t } = useTranslation();

  const principles = t("aboutPage.principles", { returnObjects: true }) as Array<{
    title: string;
    body: string;
  }>;

  const steps = t("aboutPage.steps", { returnObjects: true }) as Array<{
    title: string;
    description: string;
  }>;

  return (
    <SiteLayout>
      <Seo
        pathname="/about"
        title={t("aboutPage.tag1")}
        description={t("aboutPage.seoDescription")}
      />
      <Container className="py-16 md:py-20">
        <div className="flex flex-wrap gap-2">
          <Tag className="bg-accent/10 border-accent/20 text-accent">{t("aboutPage.tag1")}</Tag>
          <Tag>{t("aboutPage.tag2")}</Tag>
        </div>
        <h1 className="mt-8 font-display text-5xl tracking-tight md:text-7xl text-gradient">{t("aboutPage.title")}</h1>
        <p className="mt-6 max-w-[76ch] text-lg text-muted md:text-xl leading-relaxed">
          {t("aboutPage.description")}
        </p>

        <div className="mt-16 grid gap-6 md:grid-cols-3">
          {principles.map((p) => (
            <section key={p.title} className="border border-border/50 bg-black/40 backdrop-blur-md p-8 hover:border-accent transition-colors">
              <h2 className="text-xl font-display font-bold tracking-tight text-white">{p.title}</h2>
              <p className="mt-4 text-sm text-muted leading-relaxed">{p.body}</p>
            </section>
          ))}
        </div>

        <section className="mt-20 border border-border/50 bg-black p-10 md:p-14 relative overflow-hidden">
          <div className="absolute top-0 right-0 w-full h-full bg-gradient-to-b from-transparent to-primary/5 pointer-events-none" />
          <SectionHeader
            eyebrow={t("aboutPage.howWeWorkEyebrow")}
            title={t("aboutPage.howWeWorkTitle")}
            description={t("aboutPage.howWeWorkDescription")}
          />
          <ol className="mt-12 grid gap-6 md:grid-cols-4 relative z-10">
            {steps.map((s, i) => (
              <li key={s.title} className="border border-border/40 bg-bg/40 backdrop-blur-sm p-6 hover:bg-bg/60 transition-colors relative">
                <div className="absolute -top-3 -left-3 w-8 h-8 bg-accent text-black font-bold flex items-center justify-center text-xs shadow-[2px_2px_0px_rgba(255,255,255,0.2)]">0{i+1}</div>
                <div className="text-[10px] font-bold uppercase tracking-widest text-accent mt-2">{s.title}</div>
                <div className="mt-3 text-sm text-muted leading-relaxed">{s.description}</div>
              </li>
            ))}
          </ol>
          <div className="mt-12 flex flex-wrap gap-4 relative z-10">
            <Button to="/services" variant="secondary">
              {t("aboutPage.exploreServices")}
            </Button>
            <Button to="/contact" variant="primary" className="button-glow">
              {t("aboutPage.bookConsult")}
            </Button>
          </div>
        </section>
      </Container>
    </SiteLayout>
  );
}

