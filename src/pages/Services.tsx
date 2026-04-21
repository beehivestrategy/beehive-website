import { useMemo } from "react";
import { motion } from "framer-motion";
import { useTranslation } from "react-i18next";
import SiteLayout from "@/components/layout/SiteLayout";
import Container from "@/components/ui/Container";
import Button from "@/components/ui/Button";
import SectionHeader from "@/components/sections/SectionHeader";
import Tag from "@/components/ui/Tag";
import Seo from "@/components/seo/Seo";
import { services } from "@/content/services";

const containerVariants = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: {
      staggerChildren: 0.1,
    },
  },
};

const itemVariants = {
  hidden: { opacity: 0, y: 20 },
  visible: {
    opacity: 1,
    y: 0,
    transition: {
      type: "spring" as const,
      stiffness: 100,
    },
  },
};

export default function Services() {
  const { t } = useTranslation();
  
  const jsonLd = useMemo(
    () => ({
      "@context": "https://schema.org",
      "@type": "ItemList",
      itemListElement: services.map((s, index) => ({
        "@type": "ListItem",
        position: index + 1,
        url: `/services/${s.slug}`,
        name: t(`services.${s.slug}.title`, { defaultValue: s.title }),
      })),
    }),
    [t],
  );

  return (
    <SiteLayout>
      <Seo
        pathname="/services"
        title={t("home.servicesSection.eyebrow", "Services")}
        description={t("home.servicesSection.description", "Data enablement, analytics, transformation, and AI enablement services designed for measurable outcomes and enterprise governance.")}
        jsonLd={jsonLd}
      />
      <Container className="py-16 md:py-20 relative">
        <div className="absolute top-0 right-0 w-96 h-96 bg-accent/5 rounded-full blur-[100px] -z-10" />
        
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
        >
          <SectionHeader
            eyebrow={t("home.servicesSection.eyebrow", "Services")}
            title={t("home.servicesSection.title", "A clear set of offerings, designed to compound value")}
            description={t("home.servicesSection.description", "Choose a service to see outcomes, deliverables, and how we work. Each engagement is designed to be measurable, governable, and repeatable.")}
          />
        </motion.div>

        <motion.div 
          className="mt-14 grid gap-6 md:grid-cols-2"
          variants={containerVariants}
          initial="hidden"
          animate="visible"
        >
          {services.map((s) => {
            const title = t(`services.${s.slug}.title`, { defaultValue: s.title });
            const summary = t(`services.${s.slug}.summary`, { defaultValue: s.summary });
            const outcomes = t(`services.${s.slug}.outcomes`, { returnObjects: true, defaultValue: s.outcomes }) as string[];

            return (
              <motion.article 
                key={s.slug} 
                variants={itemVariants}
                className="rounded-3xl border border-border/50 glass-card p-8 hover:border-accent/30 transition-colors duration-300 relative overflow-hidden group"
              >
                <div className="absolute inset-0 bg-gradient-to-br from-accent/0 to-accent/0 group-hover:from-accent/[0.03] group-hover:to-transparent transition-colors duration-500" />
                
                <h2 className="text-2xl font-display font-semibold tracking-tight relative z-10">{title}</h2>
                <p className="mt-3 text-base text-muted leading-relaxed relative z-10">{summary}</p>

                <div className="mt-6 flex flex-wrap gap-2 relative z-10">
                  {outcomes.slice(0, 3).map((o) => (
                    <Tag key={o} className="bg-bg/50">{o}</Tag>
                  ))}
                </div>

                <div className="mt-8 flex flex-wrap items-center gap-4 relative z-10">
                  <Button to={`/services/${s.slug}`} variant="secondary">
                    {t("home.exploreServices", "View details")}
                  </Button>
                  <Button to="/contact" variant="ghost" className="text-accent hover:text-accent hover:bg-accent/10">
                    {t("nav.contact", "Talk to us")}
                  </Button>
                </div>
              </motion.article>
            );
          })}
        </motion.div>

        <motion.section 
          initial={{ opacity: 0, y: 40 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, margin: "-100px" }}
          transition={{ duration: 0.8 }}
          className="mt-20 rounded-[2.5rem] border border-border/50 glass-card p-10 md:p-14 relative overflow-hidden"
        >
          <div className="absolute top-0 right-0 w-full h-full bg-gradient-to-b from-transparent to-primary/5 pointer-events-none" />
          
          <h2 className="font-display text-3xl tracking-tight md:text-4xl text-gradient inline-block">{t("servicesPage.engagementModels.title", "Engagement models")}</h2>
          <div className="mt-10 grid gap-6 md:grid-cols-2">
            <div className="rounded-2xl border border-border/40 bg-bg/40 backdrop-blur-sm p-6 hover:bg-bg/60 transition-colors">
              <div className="text-base font-semibold text-fg font-display">{t("servicesPage.engagementModels.model1.title", "Discovery + roadmap")}</div>
              <p className="mt-2 text-sm text-muted leading-relaxed">
                {t("servicesPage.engagementModels.model1.description", "A focused engagement to clarify scope, constraints, and sequencing—so delivery starts with confidence.")}
              </p>
            </div>
            <div className="rounded-2xl border border-border/40 bg-bg/40 backdrop-blur-sm p-6 hover:bg-bg/60 transition-colors">
              <div className="text-base font-semibold text-fg font-display">{t("servicesPage.engagementModels.model2.title", "Delivery sprints")}</div>
              <p className="mt-2 text-sm text-muted leading-relaxed">
                {t("servicesPage.engagementModels.model2.description", "2–4 week increments to build foundations and ship outcomes. Includes governance, documentation, and handover.")}
              </p>
            </div>
            <div className="rounded-2xl border border-border/40 bg-bg/40 backdrop-blur-sm p-6 hover:bg-bg/60 transition-colors">
              <div className="text-base font-semibold text-fg font-display">{t("servicesPage.engagementModels.model3.title", "Retained advisory")}</div>
              <p className="mt-2 text-sm text-muted leading-relaxed">
                {t("servicesPage.engagementModels.model3.description", "Executive-level support for prioritization, risk decisions, and operating model design during transformation.")}
              </p>
            </div>
            <div className="rounded-2xl border border-border/40 bg-bg/40 backdrop-blur-sm p-6 hover:bg-bg/60 transition-colors">
              <div className="text-base font-semibold text-fg font-display">{t("servicesPage.engagementModels.model4.title", "Build–operate–transfer")}</div>
              <p className="mt-2 text-sm text-muted leading-relaxed">
                {t("servicesPage.engagementModels.model4.description", "We build with your team, help operationalize, then transition ownership with playbooks and training.")}
              </p>
            </div>
          </div>
        </motion.section>
      </Container>
    </SiteLayout>
  );
}

