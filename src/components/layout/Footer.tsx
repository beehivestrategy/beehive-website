import { Link } from "react-router-dom";
import { useTranslation } from "react-i18next";
import Container from "@/components/ui/Container";
import Button from "@/components/ui/Button";
import { site } from "@/content/site";
import BrandLogo from "@/components/brand/BrandLogo";

export default function Footer() {
  const { t } = useTranslation();

  return (
    <footer className="border-t border-border/80 relative overflow-hidden mt-10">
      <div className="absolute bottom-0 left-0 right-0 h-64 bg-gradient-to-t from-primary/5 to-transparent pointer-events-none" />
      <Container className="py-16 relative z-10">
        <div className="grid gap-10 md:grid-cols-[1.2fr_0.8fr] md:gap-12">
          <div>
            <div className="flex items-center gap-4">
              <div className="grid h-12 w-12 place-items-center border border-border bg-card overflow-hidden">
                <BrandLogo variant="mark" className="h-10 w-10" />
              </div>
              <div>
                <div className="font-display text-2xl tracking-tight text-fg">{t("site.name", { defaultValue: site.name })}</div>
                <div className="mt-1 text-xs font-bold uppercase tracking-widest text-muted">{t("site.tagline", { defaultValue: site.tagline })}</div>
              </div>
            </div>
            <div className="mt-8 flex flex-wrap items-center gap-4">
              <Button to="/contact" variant="primary" className="button-glow">
                {t('forms.leadTitle')}
              </Button>
              <Button href={`mailto:${site.contactEmail}`} variant="secondary">
                {site.contactEmail}
              </Button>
            </div>
          </div>
          <div className="grid grid-cols-2 gap-8 text-sm">
            <div className="grid gap-4">
              <div className="text-[10px] font-bold uppercase tracking-widest text-muted">{t('nav.explore')}</div>
              <Link className="text-muted hover:text-accent transition-colors py-1 block" to="/services">
                {t('nav.services')}
              </Link>
              <Link className="text-muted hover:text-accent transition-colors py-1 block" to="/industries">
                {t('nav.industries')}
              </Link>
              <Link className="text-muted hover:text-accent transition-colors py-1 block" to="/case-studies">
                {t('nav.caseStudies')}
              </Link>
              <Link className="text-muted hover:text-accent transition-colors py-1 block" to="/insights">
                {t('nav.insights')}
              </Link>
            </div>
            <div className="grid gap-4">
              <div className="text-[10px] font-bold uppercase tracking-widest text-muted">{t('nav.company')}</div>
              <Link className="text-muted hover:text-accent transition-colors py-1 block" to="/about">
                {t('nav.about')}
              </Link>
              <Link className="text-muted hover:text-accent transition-colors py-1 block" to="/contact">
                {t('nav.contact')}
              </Link>
              <Link className="text-muted hover:text-accent transition-colors py-1 block" to="/privacy">
                {t('nav.privacy')}
              </Link>
              <Link className="text-muted hover:text-accent transition-colors py-1 block" to="/accessibility">
                {t('nav.accessibility')}
              </Link>
            </div>
          </div>
        </div>
        <div className="mt-16 flex flex-col gap-2 border-t border-border/50 pt-8 text-xs text-muted md:flex-row md:items-center md:justify-between">
          <div>© {new Date().getFullYear()} {t("site.legalName", { defaultValue: site.legalName })}. All rights reserved.</div>
          <div className="flex flex-wrap gap-x-6 gap-y-4">
            <a className="hover:text-accent transition-colors py-1 inline-block" href={`mailto:${site.contactEmail}`}>
              {t('nav.contact')}
            </a>
            <Link className="hover:text-accent transition-colors py-1 inline-block" to="/privacy">
              {t('nav.privacy')}
            </Link>
            <Link className="hover:text-accent transition-colors py-1 inline-block" to="/accessibility">
              {t('nav.accessibility')}
            </Link>
          </div>
        </div>
      </Container>
    </footer>
  );
}
