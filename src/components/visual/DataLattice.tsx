import { cn } from "@/lib/utils";

type DataLatticeProps = {
  className?: string;
  variant?: "hero" | "section";
};

export default function DataLattice({ className, variant = "hero" }: DataLatticeProps) {
  return (
    <div
      aria-hidden="true"
      className={cn(
        "relative overflow-hidden rounded-3xl border border-border bg-card/40",
        variant === "hero" ? "min-h-[320px]" : "min-h-[220px]",
        className,
      )}
    >
      <div className="absolute inset-0 opacity-[0.85]">
        <div className="absolute -inset-24 bg-[radial-gradient(circle_at_20%_15%,rgb(var(--accent)/0.25),transparent_55%),radial-gradient(circle_at_80%_30%,rgb(var(--cta)/0.18),transparent_55%),radial-gradient(circle_at_45%_85%,rgb(255_255_255/0.08),transparent_55%)]" />
        <div className="absolute inset-0 bg-[linear-gradient(to_bottom,rgb(0_0_0/0.15),transparent_30%,rgb(0_0_0/0.35))]" />
        <div className="absolute inset-0 bg-[repeating-linear-gradient(90deg,rgb(255_255_255/0.06)_0px,rgb(255_255_255/0.06)_1px,transparent_1px,transparent_56px)]" />
        <div className="absolute inset-0 bg-[repeating-linear-gradient(0deg,rgb(255_255_255/0.05)_0px,rgb(255_255_255/0.05)_1px,transparent_1px,transparent_56px)]" />
      </div>

      <div className="absolute inset-0">
        <svg className="h-full w-full" viewBox="0 0 800 480" preserveAspectRatio="none">
          <defs>
            <linearGradient id="a" x1="0" x2="1" y1="0" y2="1">
              <stop offset="0" stopColor="rgb(0 230 200 / 0.45)" />
              <stop offset="1" stopColor="rgb(255 124 62 / 0.28)" />
            </linearGradient>
          </defs>
          <path
            d="M40 380 C140 280, 260 440, 360 320 C460 200, 560 360, 760 120"
            fill="none"
            stroke="url(#a)"
            strokeWidth="2"
            opacity="0.9"
          />
          <path
            d="M40 120 C170 260, 260 120, 400 260 C540 400, 620 220, 760 360"
            fill="none"
            stroke="rgb(255 255 255 / 0.18)"
            strokeWidth="1.5"
          />
          {[
            [120, 320],
            [220, 240],
            [320, 360],
            [420, 200],
            [520, 280],
            [640, 160],
            [700, 120],
            [560, 360],
          ].map(([x, y]) => (
            <g key={`${x}-${y}`}>
              <circle cx={x} cy={y} r="6" fill="rgb(var(--accent) / 0.9)" />
              <circle cx={x} cy={y} r="18" fill="rgb(var(--accent) / 0.10)" />
            </g>
          ))}
        </svg>
      </div>

      <div className="absolute inset-0 bg-[radial-gradient(circle_at_50%_50%,transparent_40%,rgb(0_0_0/0.42)_100%)]" />
    </div>
  );
}

