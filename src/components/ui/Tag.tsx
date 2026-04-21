import type React from "react";
import { cn } from "@/lib/utils";

type TagProps = {
  children: React.ReactNode;
  className?: string;
};

export default function Tag({ children, className }: TagProps) {
  return (
    <div
      className={cn(
        "inline-flex items-center justify-center border border-border bg-card px-3 py-1.5 text-[10px] font-bold uppercase tracking-widest text-fg",
        className,
      )}
    >
      {children}
    </div>
  );
}
