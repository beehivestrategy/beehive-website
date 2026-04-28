import type React from "react";
import { useId, useMemo, useState } from "react";
import { ChevronDown } from "lucide-react";
import { useTranslation } from "react-i18next";
import Button from "@/components/ui/Button";
import { cn } from "@/lib/utils";

type LeadTopic =
  | "data-enablement"
  | "analytics"
  | "transformation"
  | "ai-enablement"
  | "governance"
  | "other";

type LeadFormProps = {
  className?: string;
  compact?: boolean;
  defaultTopic?: LeadTopic;
  source?: string;
};

type FormState = {
  fullName: string;
  workEmail: string;
  company: string;
  role: string;
  topic: LeadTopic;
  message: string;
  consent: boolean;
  website: string;
};

type FieldErrors = Partial<Record<keyof FormState, string>>;

const emailRe = /^[^\s@]+@[^\s@]+\.[^\s@]+$/i;

function isRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === "object" && value !== null;
}

function validate(state: FormState, t: (key: string) => string): FieldErrors {
  const errors: FieldErrors = {};
  if (!state.fullName.trim()) errors.fullName = t("forms.leadErrors.fullName");
  if (!state.workEmail.trim()) errors.workEmail = t("forms.leadErrors.workEmail");
  else if (!emailRe.test(state.workEmail)) errors.workEmail = t("forms.leadErrors.invalidEmail");
  if (!state.company.trim()) errors.company = t("forms.leadErrors.company");
  if (!state.message.trim()) errors.message = t("forms.leadErrors.message");
  if (!state.consent) errors.consent = t("forms.leadErrors.consent");
  if (state.website.trim()) errors.website = t("forms.leadErrors.invalidSubmission");
  return errors;
}

export default function LeadForm({ className, compact, defaultTopic, source }: LeadFormProps) {
  const { t } = useTranslation();
  const formId = useId();
  const [submitting, setSubmitting] = useState(false);
  const [success, setSuccess] = useState<string | null>(null);
  const [errors, setErrors] = useState<FieldErrors>({});
  const [state, setState] = useState<FormState>({
    fullName: "",
    workEmail: "",
    company: "",
    role: "",
    topic: defaultTopic ?? "data-enablement",
    message: "",
    consent: false,
    website: "",
  });

  const errorSummary = useMemo(() => Object.values(errors).filter(Boolean), [errors]);

  async function onSubmit(e: React.FormEvent) {
    e.preventDefault();
    setSuccess(null);

    const nextErrors = validate(state, t);
    setErrors(nextErrors);
    if (Object.keys(nextErrors).length > 0) return;

    setSubmitting(true);
    try {
      const res = await fetch("/api/leads", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ ...state, source }),
      });
      const json: unknown = await res.json().catch(() => null);
      const ok = isRecord(json) && json.success === true;
      if (!res.ok || !ok) {
        const msg =
          isRecord(json) && typeof json.error === "string" ? json.error : t("forms.leadErrors.submissionFailed");
        setSuccess(null);
        setErrors({ message: msg });
        return;
      }

      setErrors({});
      setSuccess(t("forms.leadSuccess"));

      // Push event to GTM dataLayer for conversion tracking
      if (typeof window !== 'undefined') {
        (window as any).dataLayer = (window as any).dataLayer || [];
        (window as any).dataLayer.push({
          event: "generate_lead",
          lead_type: source,
          topic: state.topic
        });
      }

      setState((s) => ({
        ...s,
        message: "",
        consent: false,
        website: "",
      }));
    } catch {
      setErrors({ message: t("forms.leadErrors.submissionFailed") });
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <form
      className={cn(
        "rounded-none border border-border/60 bg-black/40 backdrop-blur-md p-6 md:p-8",
        compact ? "p-6" : "p-8 md:p-10",
        className,
      )}
      onSubmit={onSubmit}
      aria-describedby={errorSummary.length ? `${formId}-errors` : undefined}
    >
      <div className="grid gap-2">
        <h2 className="font-display text-2xl font-bold tracking-tight text-white">
          {compact ? t("forms.leadEmail") : t("forms.leadTitle")}
        </h2>
        <p className="text-sm text-muted leading-relaxed">
          {t("forms.leadSubtitle")}
        </p>
      </div>

      {errorSummary.length ? (
        <div
          id={`${formId}-errors`}
          className="mt-5 rounded-2xl border border-cta/30 bg-cta/10 p-4 text-sm text-fg"
          role="alert"
        >
          <div className="font-semibold">{t("forms.leadErrors.fixErrors")}</div>
          <ul className="mt-2 list-disc pl-5">
            {errorSummary.map((err, idx) => (
              <li key={`${idx}-${err}`}>{err}</li>
            ))}
          </ul>
        </div>
      ) : null}

      <div className={cn("mt-6 grid gap-4", compact ? "grid-cols-1" : "grid-cols-1 md:grid-cols-2")}>
        <label className={cn("grid gap-2 text-sm font-bold uppercase tracking-widest text-muted text-[10px]", compact ? "" : "col-span-1 md:col-span-2")}>
          {t("forms.fullName")}
          <input
            name="name"
            autoComplete="name"
            spellCheck={false}
            className={cn(
              "h-12 w-full rounded-none border bg-bg/50 px-4 text-sm text-fg placeholder:text-muted focus:border-accent focus:outline-none focus:ring-1 focus:ring-accent disabled:opacity-50 transition-colors font-normal normal-case tracking-normal",
              errors.fullName ? "border-cta" : "border-border/60",
            )}
            disabled={submitting}
            value={state.fullName}
            onChange={(e) => setState((s) => ({ ...s, fullName: e.target.value }))}
          />
        </label>

        <label className={cn("grid gap-2 text-sm font-bold uppercase tracking-widest text-muted text-[10px]", compact ? "" : "col-span-1 md:col-span-2")}>
          {t("forms.workEmail")}
          <input
            name="email"
            type="email"
            autoComplete="email"
            spellCheck={false}
            inputMode="email"
            className={cn(
              "h-12 w-full rounded-none border bg-bg/50 px-4 text-sm text-fg placeholder:text-muted focus:border-accent focus:outline-none focus:ring-1 focus:ring-accent disabled:opacity-50 transition-colors font-normal normal-case tracking-normal",
              errors.workEmail ? "border-cta" : "border-border/60",
            )}
            disabled={submitting}
            value={state.workEmail}
            onChange={(e) => setState((s) => ({ ...s, workEmail: e.target.value }))}
          />
        </label>

        <label className={cn("grid gap-2 text-sm font-bold uppercase tracking-widest text-muted text-[10px]", compact ? "" : "col-span-1 md:col-span-1")}>
          {t("forms.company")}
          <input
            name="company"
            type="text"
            autoComplete="organization"
            spellCheck={false}
            className={cn(
              "h-12 w-full rounded-none border bg-bg/50 px-4 text-sm text-fg placeholder:text-muted focus:border-accent focus:outline-none focus:ring-1 focus:ring-accent disabled:opacity-50 transition-colors font-normal normal-case tracking-normal",
              errors.company ? "border-cta" : "border-border/60",
            )}
            disabled={submitting}
            value={state.company}
            onChange={(e) => setState((s) => ({ ...s, company: e.target.value }))}
          />
        </label>

        <label className={cn("grid gap-2 text-sm font-bold uppercase tracking-widest text-muted text-[10px]", compact ? "" : "col-span-1 md:col-span-1")}>
          {t("forms.role")}
          <input
            name="role"
            type="text"
            autoComplete="organization-title"
            spellCheck={false}
            className="h-12 w-full rounded-none border border-border/60 bg-bg/50 px-4 text-sm text-fg placeholder:text-muted focus:border-accent focus:outline-none focus:ring-1 focus:ring-accent disabled:opacity-50 transition-colors font-normal normal-case tracking-normal"
            disabled={submitting}
            value={state.role}
            onChange={(e) => setState((s) => ({ ...s, role: e.target.value }))}
          />
        </label>

        <label className={cn("grid gap-2 text-sm font-bold uppercase tracking-widest text-muted text-[10px]", compact ? "" : "col-span-1 md:col-span-2")}>
          {t("forms.topic")}
          <div className="relative">
            <select
              name="topic"
              autoComplete="off"
              className={cn(
                "h-12 w-full appearance-none rounded-none border bg-bg/50 px-4 text-sm text-fg placeholder:text-muted focus:border-accent focus:outline-none focus:ring-1 focus:ring-accent disabled:opacity-50 transition-colors font-normal normal-case tracking-normal",
                errors.topic ? "border-cta" : "border-border/60",
              )}
              disabled={submitting}
              value={state.topic}
              onChange={(e) => setState((s) => ({ ...s, topic: e.target.value as LeadTopic }))}
            >
              <option value="data-enablement">Data enablement</option>
              <option value="analytics">Analytics enablement</option>
              <option value="transformation">Transformation</option>
              <option value="ai-enablement">AI enablement</option>
              <option value="governance">Governance</option>
              <option value="other">Other</option>
            </select>
            <div className="pointer-events-none absolute inset-y-0 right-4 grid place-items-center">
              <ChevronDown aria-hidden="true" className="h-4 w-4 text-muted" />
            </div>
          </div>
        </label>

        <label className={cn("grid gap-2 text-sm font-bold uppercase tracking-widest text-muted text-[10px]", compact ? "" : "col-span-1 md:col-span-2")}>
          {t("forms.message")}
          <textarea
            name="message"
            className={cn(
              "min-h-28 w-full resize-y rounded-none border bg-bg/50 px-4 py-3 text-sm text-fg placeholder:text-muted focus:border-accent focus:outline-none focus:ring-1 focus:ring-accent disabled:opacity-50 transition-colors font-normal normal-case tracking-normal",
              errors.message ? "border-cta" : "border-border/60",
            )}
            disabled={submitting}
            value={state.message}
            onChange={(e) => setState((s) => ({ ...s, message: e.target.value }))}
          />
        </label>

        <label className="sr-only" aria-hidden="true">
          Website
          <input
            name="website"
            type="text"
            tabIndex={-1}
            autoComplete="off"
            value={state.website}
            onChange={(e) => setState((s) => ({ ...s, website: e.target.value }))}
          />
        </label>

        <div className="flex gap-3 items-start mt-2 col-span-1 md:col-span-2">
          <input
            id={`${formId}-consent`}
            name="consent"
            type="checkbox"
            disabled={submitting}
            checked={state.consent}
            onChange={(e) => setState((s) => ({ ...s, consent: e.target.checked }))}
            className="mt-1 h-4 w-4 rounded-none border-border/60 bg-bg/50 text-accent focus:ring-accent accent-accent accent-bg-accent"
          />
          <label htmlFor={`${formId}-consent`} className="text-sm text-muted leading-relaxed">
            {t('forms.consent')}
          </label>
        </div>
      </div>

      {success ? (
        <div className="mt-4 rounded-none border border-accent/30 bg-accent/5 p-4 text-sm font-bold text-accent flex items-center gap-3" role="status" aria-live="polite">
          <svg aria-hidden="true" xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="shrink-0"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><path d="m9 11 3 3L22 4"/></svg>
          {success}
        </div>
      ) : null}
      
      <Button type="submit" variant="primary" className="w-full justify-center button-glow rounded-none h-14 mt-4 text-sm" disabled={submitting}>
        {submitting ? t("forms.sending") : t("forms.send")}
      </Button>
    </form>
  );
}
