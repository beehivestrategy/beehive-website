import { useEffect } from "react";
import { useLocation } from "react-router-dom";

// Define the global dataLayer type to prevent TypeScript errors
declare global {
  interface Window {
    dataLayer: Record<string, any>[];
  }
}

export default function GTMTracker() {
  const location = useLocation();

  useEffect(() => {
    // Initialize dataLayer if it doesn't exist
    window.dataLayer = window.dataLayer || [];
    
    // Push the custom virtual_page_view event
    window.dataLayer.push({
      event: "virtual_page_view",
      page_path: location.pathname + location.search,
      page_title: document.title,
    });
  }, [location]);

  // This component doesn't render anything visible
  return null;
}
