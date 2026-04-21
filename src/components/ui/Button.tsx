import type React from "react";
import { Link } from "react-router-dom";
import { cn } from "@/lib/utils";

type ButtonVariant = "primary" | "secondary" | "ghost";
type ButtonSize = "sm" | "md" | "lg";

type BaseProps = {
  variant?: ButtonVariant;
  size?: ButtonSize;
  className?: string;
  children: React.ReactNode;
};

type ButtonAsButton = BaseProps &
  Omit<React.ButtonHTMLAttributes<HTMLButtonElement>, "className" | "children"> & { href?: never; to?: never };

type ButtonAsLink = BaseProps &
  Omit<React.AnchorHTMLAttributes<HTMLAnchorElement>, "className" | "children" | "href"> & { href: string; to?: never };

type ButtonAsRouterLink = BaseProps &
  Omit<React.ComponentPropsWithoutRef<typeof Link>, "className" | "children" | "to"> & { to: string; href?: never };

export type ButtonProps = ButtonAsButton | ButtonAsLink | ButtonAsRouterLink;

const base =
  "inline-flex items-center justify-center gap-2 border px-6 py-4 font-bold tracking-widest uppercase text-xs transition-[color,background-color,border-color,text-decoration-color,fill,stroke,box-shadow,transform] active:scale-[0.98] focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[rgb(var(--focus))] focus-visible:ring-offset-2 focus-visible:ring-offset-bg relative overflow-hidden";

const variants: Record<ButtonVariant, string> = {
  primary:
    "border-transparent bg-accent text-black hover:bg-white hover:text-black shadow-[4px_4px_0px_rgb(255,255,255)] hover:shadow-[2px_2px_0px_rgb(255,255,255)] hover:translate-x-[2px] hover:translate-y-[2px]",
  secondary: "border-border/60 bg-card text-fg hover:border-accent hover:text-accent hover:bg-card shadow-sm",
  ghost: "border-transparent bg-transparent text-fg hover:bg-white/5",
};

const sizes: Record<ButtonSize, string> = {
  sm: "h-10 px-4 text-[10px]",
  md: "h-12 px-6",
  lg: "h-14 px-8 text-xs",
};

export default function Button(props: ButtonProps) {
  const { variant = "secondary", size = "md", className, children, ...rest } = props;
  const classes = cn(base, variants[variant], sizes[size], className);

  if ("to" in props) {
    const { to, ...linkProps } = rest as Omit<ButtonAsRouterLink, keyof BaseProps>;
    return (
      <Link className={classes} to={to} {...linkProps}>
        {children}
      </Link>
    );
  }

  if ("href" in props) {
    const { href, ...anchorProps } = rest as Omit<ButtonAsLink, keyof BaseProps>;
    return (
      <a className={classes} href={href} {...anchorProps}>
        {children}
      </a>
    );
  }

  const buttonProps = rest as Omit<ButtonAsButton, keyof BaseProps>;
  return (
    <button className={classes} {...buttonProps}>
      {children}
    </button>
  );
}
