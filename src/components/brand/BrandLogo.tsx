import { useMemo, useState } from "react";
import { useTranslation } from "react-i18next";
import LogoMark from "@/components/brand/LogoMark";

type BrandLogoProps = {
  variant?: "mark" | "horizontal";
  className?: string;
};

export default function BrandLogo({ variant = "horizontal", className }: BrandLogoProps) {
  const { t } = useTranslation();
  const [failed, setFailed] = useState(false);

  const src = useMemo(() => {
    if (variant === "mark") return "/brand/logo-mark.png";
    return "/brand/logo-horizontal.png";
  }, [variant]);

  if (failed) {
    return <LogoMark className={className} />;
  }

  return (
    <img
      src={src}
      alt={t("site.name")}
      className={className}
      onError={() => setFailed(true)}
      loading="eager"
      decoding="async"
    />
  );
}
