import { useEffect } from "react";
import { useTranslation } from "react-i18next";
import { site } from "@/content/site";
import { ensureLinkRel, ensureMetaTag, getBaseJsonLd, getDefaultOgImage, toCanonicalUrl } from "@/utils/seo";

type SeoProps = {
  title?: string;
  description?: string;
  pathname: string;
  image?: string;
  ogType?: "website" | "article";
  publishedTime?: string;
  jsonLd?: Record<string, unknown> | Array<Record<string, unknown>>;
};

function upsertJsonLd(id: string, data: Record<string, unknown> | Array<Record<string, unknown>>) {
  const existing = document.getElementById(id);
  const el = existing ?? document.createElement("script");
  el.setAttribute("type", "application/ld+json");
  el.setAttribute("id", id);
  el.textContent = JSON.stringify(data);
  if (!existing) document.head.appendChild(el);
}

export default function Seo({ title, description, pathname, image, ogType = "website", publishedTime, jsonLd }: SeoProps) {
  const { t } = useTranslation();

  useEffect(() => {
    const siteName = t("site.name", { defaultValue: site.name });
    const siteTagline = t("site.tagline", { defaultValue: site.tagline });
    const siteDescription = t("site.description", { defaultValue: site.description });

    const pageTitle = title ? `${title} | ${siteName}` : `${siteName} | ${siteTagline}`;
    const pageDescription = description ?? siteDescription;
    const canonical = toCanonicalUrl(pathname);
    const ogImage = image ?? getDefaultOgImage();

    document.title = pageTitle;
    ensureLinkRel("canonical", canonical);

    ensureMetaTag("description", pageDescription);
    ensureMetaTag("og:type", ogType, true);
    ensureMetaTag("og:site_name", siteName, true);
    ensureMetaTag("og:title", pageTitle, true);
    ensureMetaTag("og:description", pageDescription, true);
    ensureMetaTag("og:url", canonical, true);
    ensureMetaTag("og:image", ogImage, true);
    
    if (ogType === "article" && publishedTime) {
      ensureMetaTag("article:published_time", publishedTime, true);
    }

    ensureMetaTag("twitter:card", "summary_large_image");
    ensureMetaTag("twitter:title", pageTitle);
    ensureMetaTag("twitter:description", pageDescription);
    ensureMetaTag("twitter:image", ogImage);

    const baseJsonLd = getBaseJsonLd();
    const combinedJsonLd = jsonLd
      ? Array.isArray(jsonLd)
        ? [...baseJsonLd, ...jsonLd]
        : [...baseJsonLd, jsonLd]
      : baseJsonLd;

    upsertJsonLd("jsonld-primary", combinedJsonLd);
  }, [title, description, pathname, image, ogType, publishedTime, jsonLd, t]);

  return null;
}
