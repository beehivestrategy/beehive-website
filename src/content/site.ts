export const site = {
  name: "Beehive",
  legalName: "Beehive Data & AI Consulting",
  tagline: "Data, Analytics & AI Transformation",
  description:
    "Data enablement, analytics, transformation, and AI enablement consulting. Build trusted data foundations, accelerate insight delivery, and operationalize AI with governance.",
  defaultLocale: "en",
  contactEmail: "hello@beehive.consulting",
};

export function getSiteOrigin(): string {
  if (typeof window === "undefined") return "https://example.com";
  return window.location.origin;
}

