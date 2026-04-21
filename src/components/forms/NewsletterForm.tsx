import type React from "react";
import { useId, useMemo, useState } from "react";
import Button from "@/components/ui/Button";
import { cn } from "@/lib/utils";
import { CheckCircle2 } from "lucide-react";
import { useTranslation } from "react-i18next";

type NewsletterFormProps = {
  className?: string;
  source?: string;
};

const emailRe = /^[^\s@]+@[^\s@]+\.[^\s@]+$/i;

function isRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === "object" && value !== null;
}

export default function NewsletterForm({ className, source }: NewsletterFormProps) {
  const { t } = useTranslation();
  const id = useId();
  const [email, setEmail] = useState("");
  const [submitting, setSubmitting] = useState(false);
  const [success, setSuccess] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const hasError = useMemo(() => Boolean(error), [error]);

  async function onSubmit(e: React.FormEvent) {
    e.preventDefault();
    setSuccess(null);
    setError(null);

    const trimmed = email.trim();
    if (!trimmed) {
      setError(t("forms.newsletterErrors.emptyEmail"));
      return;
    }
    if (!emailRe.test(trimmed)) {
      setError(t("forms.newsletterErrors.invalidEmail"));
      return;
    }

    setSubmitting(true);
    try {
      const res = await fetch("/api/newsletter", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email: trimmed, source }),
      });
      const json: unknown = await res.json().catch(() => null);
      const ok = isRecord(json) && json.success === true;
      if (!res.ok || !ok) {
        setError(t("forms.newsletterErrors.submissionFailed"));
        return;
      }
      setSuccess(t("forms.newsletterSuccess"));
      setEmail("");
    } catch {
      setError(t("forms.newsletterErrors.submissionFailed"));
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <div className={cn("rounded-none border border-border/50 bg-black/40 backdrop-blur-md p-6", className)}>
      <h3 className="font-display text-xl font-bold tracking-tight text-white">{t('forms.newsletterTitle')}</h3>
      <p className="mt-2 text-sm text-muted leading-relaxed">
        {t('forms.newsletterSubtitle')}
      </p>

      {success ? (
        <div className="mt-6 flex items-center gap-3 rounded-none border border-accent/30 bg-accent/5 p-4 text-sm font-bold text-accent">
          <CheckCircle2 aria-hidden="true" className="h-5 w-5 shrink-0" />
          {t('forms.subscribed')}
        </div>
      ) : (
        <form className="mt-6 grid gap-3" onSubmit={onSubmit}>
          <div className="grid gap-2">
            <label htmlFor={`${id}-email`} className="sr-only">
              {t('forms.leadEmail')}
            </label>
            <input
              id={`${id}-email`}
              name="email"
              type="email"
              autoComplete="email"
              spellCheck={false}
              required
              disabled={submitting}
              placeholder={t('forms.emailPlaceholder')}
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className={cn(
                "h-12 w-full rounded-none border bg-bg/50 px-4 text-sm text-fg placeholder:text-muted focus:border-accent focus:outline-none focus:ring-1 focus:ring-accent disabled:opacity-50 transition-colors",
                hasError ? "border-cta/60" : "border-border/60",
              )}
              aria-describedby={error ? `${id}-err` : undefined}
            />
          </div>

          <Button type="submit" variant="primary" className="w-full justify-center rounded-none button-glow h-12" disabled={submitting}>
            {submitting ? t('forms.subscribing') : t('forms.subscribe')}
          </Button>

          {error ? (
            <div id={`${id}-err`} className="mt-2 text-xs text-cta" role="status" aria-live="polite">
              {error}
            </div>
          ) : null}
        </form>
      )}
    </div>
  );
}
