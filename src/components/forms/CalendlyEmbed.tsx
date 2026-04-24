import { InlineWidget } from "react-calendly";

export default function CalendlyEmbed({ url = "https://calendly.com/beehivestrategy/30min" }: { url?: string }) {
  return (
    <div className="w-full h-full min-h-[650px] border border-border/60 bg-black/40 backdrop-blur-md overflow-hidden">
      <InlineWidget 
        url={url} 
        styles={{ height: "650px", width: "100%" }} 
        pageSettings={{
          backgroundColor: '0B0F14',
          hideEventTypeDetails: false,
          hideLandingPageDetails: false,
          primaryColor: '2DD4BF',
          textColor: 'FFFFFF'
        }}
      />
    </div>
  );
}
