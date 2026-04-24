import { useState } from "react";
import SiteLayout from "@/components/layout/SiteLayout";
import Container from "@/components/ui/Container";
import SectionHeader from "@/components/sections/SectionHeader";
import Seo from "@/components/seo/Seo";
import LeadForm from "@/components/forms/LeadForm";
import CalendlyEmbed from "@/components/forms/CalendlyEmbed";
import Tag from "@/components/ui/Tag";
import { site } from "@/content/site";
import { useTranslation } from "react-i18next";
import { cn } from "@/lib/utils";

export default function Contact() {
  const { t } = useTranslation();
  const [activeTab, setActiveTab] = useState<"form" | "calendar">("form");

  return (
    <SiteLayout>
      <Seo
        pathname="/contact"
        title={t("contactPage.tag1")}
        description={t("contactPage.seoDescription")}
      />
      <Container className="py-16 md:py-20">
        <div className="flex flex-wrap gap-2">
          <Tag>{t("contactPage.tag1")}</Tag>
          <Tag>{t("contactPage.tag2")}</Tag>
        </div>

        <div className="mt-6 grid gap-10 lg:grid-cols-[1fr_1fr] lg:items-start">
          <div>
            <SectionHeader
              eyebrow={t("contactPage.eyebrow")}
              title={t("contactPage.title")}
              description={t("contactPage.description")}
            />
            <div className="mt-12 grid gap-6 border border-border/50 bg-black p-8 text-sm text-muted">
              <div>
                <div className="text-[10px] font-bold uppercase tracking-widest text-accent">{t("contactPage.emailEyebrow")}</div>
                <a className="mt-2 inline-block text-base font-bold text-white hover:text-accent transition-colors" href={`mailto:${site.contactEmail}`}>
                  {site.contactEmail}
                </a>
              </div>
              <div className="border-t border-border/50 pt-6">
                <div className="text-[10px] font-bold uppercase tracking-widest text-accent">{t("contactPage.whatToInclude")}</div>
                <ul className="mt-4 grid gap-2">
                  <li className="flex gap-3 items-center">
                    <span className="h-1.5 w-1.5 bg-accent shadow-[2px_2px_0px_rgba(255,255,255,0.2)]" />
                    {t("contactPage.include1")}
                  </li>
                  <li className="flex gap-3 items-center">
                    <span className="h-1.5 w-1.5 bg-accent shadow-[2px_2px_0px_rgba(255,255,255,0.2)]" />
                    {t("contactPage.include2")}
                  </li>
                  <li className="flex gap-3 items-center">
                    <span className="h-1.5 w-1.5 bg-accent shadow-[2px_2px_0px_rgba(255,255,255,0.2)]" />
                    {t("contactPage.include3")}
                  </li>
                </ul>
              </div>
            </div>
          </div>

          <div className="flex flex-col gap-6">
            <div className="flex bg-black/40 border border-border/60 p-1">
              <button
                onClick={() => setActiveTab("form")}
                className={cn(
                  "flex-1 py-3 px-4 text-sm font-bold uppercase tracking-wider transition-colors",
                  activeTab === "form" ? "bg-accent text-black" : "text-muted hover:text-white"
                )}
              >
                Send Message
              </button>
              <button
                onClick={() => setActiveTab("calendar")}
                className={cn(
                  "flex-1 py-3 px-4 text-sm font-bold uppercase tracking-wider transition-colors",
                  activeTab === "calendar" ? "bg-accent text-black" : "text-muted hover:text-white"
                )}
              >
                Book Meeting
              </button>
            </div>
            
            {activeTab === "form" ? (
              <LeadForm source="contact" />
            ) : (
              <CalendlyEmbed url="https://calendly.com/beehivestrategy/30min" />
            )}
          </div>
        </div>
      </Container>
    </SiteLayout>
  );
}

