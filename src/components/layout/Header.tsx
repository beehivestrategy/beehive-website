import { useState, useEffect } from "react";
import { Link, useLocation } from "react-router-dom";
import { Menu, Moon, Sun, X } from "lucide-react";
import { useTheme } from "@/hooks/useTheme";
import { useTranslation } from "react-i18next";
import Button from "@/components/ui/Button";
import Container from "@/components/ui/Container";
import NavItemLink from "@/components/nav/NavItemLink";
import LogoMark from "@/components/brand/LogoMark";

function LanguageSwitcher() {
  const { i18n } = useTranslation();
  
  const toggleLanguage = () => {
    const nextLang = i18n.language === 'en' ? 'zh-CN' : i18n.language === 'zh-CN' ? 'zh-TW' : 'en';
    i18n.changeLanguage(nextLang);
  };

  const getLanguageLabel = () => {
    switch (i18n.language) {
      case 'zh-CN': return '简';
      case 'zh-TW': return '繁';
      default: return 'EN';
    }
  };

  return (
    <button
      type="button"
      className="inline-flex h-10 w-10 items-center justify-center border border-border text-muted transition hover:text-fg hover:bg-white/5 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-accent"
      onClick={toggleLanguage}
      aria-label="Toggle language"
      title={`Current: ${getLanguageLabel()}`}
    >
      <span aria-hidden="true" className="flex items-center justify-center font-bold text-xs">
        {getLanguageLabel()}
      </span>
    </button>
  );
}

export default function Header() {
  const { isDark, toggleTheme } = useTheme();
  const { t } = useTranslation();
  const [open, setOpen] = useState(false);
  const location = useLocation();

  // Close mobile menu when route changes
  useEffect(() => {
    setOpen(false);
  }, [location.pathname]);

  return (
    <header className="sticky top-0 z-50 w-full border-b border-border bg-bg/95 backdrop-blur-md">
      <div className="flex h-20 items-center justify-between px-6 md:px-12 max-w-[1600px] mx-auto w-full">
        <Link className="group flex items-center gap-3" to="/" aria-label={`${t("site.name")} home`} aria-current={location.pathname === "/" ? "page" : undefined}>
          <span className="relative grid h-10 w-10 place-items-center border border-border bg-card">
            <LogoMark className="h-8 w-8" />
          </span>
          <div className="leading-none">
            <div className="font-display text-2xl font-bold uppercase tracking-tighter text-fg">{t("site.name")}</div>
          </div>
        </Link>

        <nav className="hidden items-center gap-8 md:flex" aria-label="Primary navigation">
          <NavItemLink to="/services" className="uppercase tracking-widest text-[10px] font-bold">{t('nav.services')}</NavItemLink>
          <NavItemLink to="/industries" className="uppercase tracking-widest text-[10px] font-bold">{t('nav.industries')}</NavItemLink>
          <NavItemLink to="/case-studies" className="uppercase tracking-widest text-[10px] font-bold">{t('nav.caseStudies')}</NavItemLink>
          <NavItemLink to="/insights" className="uppercase tracking-widest text-[10px] font-bold">{t('nav.insights')}</NavItemLink>
          <NavItemLink to="/about" className="uppercase tracking-widest text-[10px] font-bold">{t('nav.about')}</NavItemLink>
          <NavItemLink to="/contact" className="uppercase tracking-widest text-[10px] font-bold">{t('nav.contact')}</NavItemLink>
        </nav>

        <div className="hidden items-center gap-4 md:flex">
          <LanguageSwitcher />
          <button
            type="button"
            className="inline-flex h-10 w-10 items-center justify-center border border-border text-muted transition hover:text-fg hover:bg-white/5 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[rgb(var(--focus))]"
            onClick={toggleTheme}
            aria-label={isDark ? "Switch to light theme" : "Switch to dark theme"}
          >
            <span aria-hidden="true">
              {isDark ? <Sun className="h-4 w-4" /> : <Moon className="h-4 w-4" />}
            </span>
          </button>
          <Button to="/contact" variant="primary" className="!h-10 !px-6">
            {t('nav.engageUs')}
          </Button>
        </div>

        <div className="flex items-center gap-4 md:hidden">
          <LanguageSwitcher />
          <button
            type="button"
            className="inline-flex h-10 w-10 items-center justify-center border border-border text-muted transition hover:text-fg hover:bg-white/5 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-accent"
            onClick={toggleTheme}
            aria-label={isDark ? "Switch to light theme" : "Switch to dark theme"}
          >
            <span aria-hidden="true">
              {isDark ? <Sun className="h-4 w-4" /> : <Moon className="h-4 w-4" />}
            </span>
          </button>
          <button
            type="button"
            className="inline-flex h-10 w-10 items-center justify-center border border-border text-muted transition hover:text-fg hover:bg-white/5 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-accent"
            onClick={() => setOpen((v) => !v)}
            aria-label={open ? "Close menu" : "Open menu"}
            aria-expanded={open}
            aria-controls="mobile-menu"
          >
            <span aria-hidden="true">
              {open ? <X className="h-5 w-5" /> : <Menu className="h-5 w-5" />}
            </span>
          </button>
        </div>
      </div>

      {open ? (
        <div id="mobile-menu" className="absolute top-full left-0 right-0 border-b border-border bg-bg/95 backdrop-blur-xl md:hidden p-6 shadow-2xl h-[calc(100vh-80px)] overflow-y-auto overscroll-contain pb-[calc(2rem+env(safe-area-inset-bottom))]">
          <div className="grid gap-6 max-w-[1600px] mx-auto pb-8">
            <NavItemLink to="/services" className="uppercase tracking-widest text-sm font-bold w-full block py-4 border-b border-border/50">{t('nav.services')}</NavItemLink>
            <NavItemLink to="/industries" className="uppercase tracking-widest text-sm font-bold w-full block py-4 border-b border-border/50">{t('nav.industries')}</NavItemLink>
            <NavItemLink to="/case-studies" className="uppercase tracking-widest text-sm font-bold w-full block py-4 border-b border-border/50">{t('nav.caseStudies')}</NavItemLink>
            <NavItemLink to="/insights" className="uppercase tracking-widest text-sm font-bold w-full block py-4 border-b border-border/50">{t('nav.insights')}</NavItemLink>
            <NavItemLink to="/about" className="uppercase tracking-widest text-sm font-bold w-full block py-4 border-b border-border/50">{t('nav.about')}</NavItemLink>
            <NavItemLink to="/contact" className="uppercase tracking-widest text-sm font-bold w-full block py-4 border-b border-border/50">{t('nav.contact')}</NavItemLink>
            <Button to="/contact" variant="primary" className="mt-8 w-full justify-center button-glow py-4 h-14">
              {t('nav.engageUs')}
            </Button>
          </div>
        </div>
      ) : null}
    </header>
  );
}
