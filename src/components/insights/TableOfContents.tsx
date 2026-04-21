import { useEffect, useState } from "react";
import { cn } from "@/lib/utils";
import { useTranslation } from "react-i18next";

type TocItem = {
  id: string;
  label: string;
};

type TableOfContentsProps = {
  items: TocItem[];
  className?: string;
};

export default function TableOfContents({ items, className }: TableOfContentsProps) {
  const { t } = useTranslation();
  const [activeId, setActiveId] = useState<string>("");

  if (!items.length) return null;

  return (
    <nav aria-label={t('misc.tableOfContents')} className={cn("border border-border/50 bg-black/40 backdrop-blur-md p-6", className)}>
      <div className="text-[10px] font-bold uppercase tracking-widest text-accent">{t('misc.onThisPage')}</div>
      <ol className="mt-5 grid gap-3 text-sm">
        {items.map((i) => (
          <li key={i.id}>
            <a className="text-muted hover:text-white transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-accent rounded-sm" href={`#${i.id}`}>
              {i.label}
            </a>
          </li>
        ))}
      </ol>
    </nav>
  );
}

