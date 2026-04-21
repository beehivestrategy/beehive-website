import type React from "react";
import { Link, useLocation } from "react-router-dom";
import { cn } from "@/lib/utils";

type NavItemLinkProps = {
  to: string;
  children: React.ReactNode;
  className?: string;
};

export default function NavItemLink({ to, children, className }: NavItemLinkProps) {
  const location = useLocation();
  const isActive = location.pathname.startsWith(to) && to !== "/" || (location.pathname === "/" && to === "/");

  return (
    <Link
      to={to}
      className={cn(
        "rounded-none px-3 py-2 text-sm font-medium transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-accent",
        isActive ? "text-accent" : "text-muted hover:text-white",
        className
      )}
      aria-current={isActive ? "page" : undefined}
    >
      {children}
    </Link>
  );
}
