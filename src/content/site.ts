export const site = {
  name: "Beehive Strategy",
  legalName: "Beehive Strategy",
  tagline: "Data, Analytics & AI Transformation",
  description:
    "Data enablement, analytics, transformation, and AI enablement consulting. Build trusted data foundations, accelerate insight delivery, and operationalize AI with governance.",
  defaultLocale: "en",
  contactEmail: "hello@beehivestrategy.com",
};

export function getSiteOrigin(): string {
  if (typeof window === "undefined") return "https://www.beehivestrategy.com";
  return window.location.origin;
}
