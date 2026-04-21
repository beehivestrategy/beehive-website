import { useTranslation } from 'react-i18next';

export default function SkipLink() {
  const { t } = useTranslation();
  
  return (
    <a
      className="sr-only focus:not-sr-only focus:fixed focus:left-6 focus:top-6 focus:z-[100] focus:rounded-full focus:bg-card focus:px-4 focus:py-2 focus:text-sm focus:text-fg focus:shadow-glow"
      href="#main"
    >
      {t('misc.skipToContent')}
    </a>
  );
}

