import type React from "react";
import Header from "@/components/layout/Header";
import Footer from "@/components/layout/Footer";
import SkipLink from "@/components/ui/SkipLink";

type SiteLayoutProps = {
  children: React.ReactNode;
};

export default function SiteLayout({ children }: SiteLayoutProps) {
  return (
    <div className="min-h-dvh relative flex flex-col">
      <div className="noise-overlay" />
      <SkipLink />
      <Header />
      <main id="main" className="flex-1 relative z-10 overflow-x-hidden">
        {children}
      </main>
      <Footer />
    </div>
  );
}
