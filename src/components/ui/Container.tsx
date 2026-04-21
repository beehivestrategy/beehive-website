import type React from "react";
import { cn } from "@/lib/utils";

type ContainerProps = {
  as?: keyof JSX.IntrinsicElements;
  className?: string;
  children: React.ReactNode;
};

export default function Container({ as, className, children }: ContainerProps) {
  const Comp = as ?? "div";
  return <Comp className={cn("mx-auto w-full max-w-[1600px] px-6 md:px-12", className)}>{children}</Comp>;
}
