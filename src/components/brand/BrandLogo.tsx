import { useMemo, useState } from "react";
import { useTranslation } from "react-i18next";
import LogoMark from "@/components/brand/LogoMark";

type BrandLogoProps = {
  variant?: "mark" | "horizontal";
  className?: string;
};

export default function BrandLogo({ variant = "horizontal", className }: BrandLogoProps) {
  const { t } = useTranslation();
  const [index, setIndex] = useState(0);

  const sources = useMemo(() => {
    if (variant === "mark") return ["/brand/logo-mark.svg", "/brand/logo-mark.png"];
    return ["/brand/logo-horizontal.svg", "/brand/logo-horizontal.png"];
  }, [variant]);

  if (index >= sources.length) {
    return <LogoMark className={className} />;
  }

  return (
    <img
      src={sources[index]}
      alt={t("site.name")}
      className={className}
      onError={() => setIndex((v) => v + 1)}
      loading="eager"
      decoding="async"
    />
  );
}
