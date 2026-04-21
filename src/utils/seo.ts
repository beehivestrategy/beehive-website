import { getSiteOrigin, site } from "@/content/site";

export function toCanonicalUrl(pathname: string): string {
  const origin = getSiteOrigin();
  const normalized = pathname.startsWith("/") ? pathname : `/${pathname}`;
  return `${origin}${normalized}`;
}

export function ensureMetaTag(nameOrProperty: string, value: string, isProperty = false) {
  const selector = isProperty ? `meta[property="${nameOrProperty}"]` : `meta[name="${nameOrProperty}"]`;
  let el = document.head.querySelector<HTMLMetaElement>(selector);
  if (!el) {
    el = document.createElement("meta");
    if (isProperty) {
      el.setAttribute("property", nameOrProperty);
    } else {
      el.setAttribute("name", nameOrProperty);
    }
    document.head.appendChild(el);
  }
  el.setAttribute("content", value);
}

export function ensureLinkRel(rel: string, href: string) {
  let el = document.head.querySelector<HTMLLinkElement>(`link[rel="${rel}"]`);
  if (!el) {
    el = document.createElement("link");
    el.setAttribute("rel", rel);
    document.head.appendChild(el);
  }
  el.setAttribute("href", href);
}

export function getDefaultOgImage(): string {
  return "https://coresg-normal.trae.ai/api/ide/v1/text_to_image?prompt=editorial%20corporate%20hero%20image%2C%20abstract%20data%20lattice%20lines%20and%20nodes%20on%20a%20near-black%20background%2C%20subtle%20grain%20texture%2C%20teal%20and%20signal-orange%20accent%20glow%2C%20high-end%20technology%20consulting%20aesthetic%2C%20clean%20negative%20space%2C%20no%20text%2C%20photoreal%20lighting%2C%20ultra%20detailed%2C%20sharp%20focus&image_size=landscape_16_9";
}

export function getOrganizationJsonLd() {
  const origin = getSiteOrigin();
  return {
    "@context": "https://schema.org",
    "@type": "Organization",
    name: site.legalName,
    url: origin,
    email: site.contactEmail,
  };
}

