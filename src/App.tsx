import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Home from "@/pages/Home";
import Services from "@/pages/Services";
import ServiceDetail from "@/pages/ServiceDetail";
import Industries from "@/pages/Industries";
import IndustryDetail from "@/pages/IndustryDetail";
import CaseStudies from "@/pages/CaseStudies";
import CaseStudyDetail from "@/pages/CaseStudyDetail";
import Insights from "@/pages/Insights";
import InsightDetail from "@/pages/InsightDetail";
import About from "@/pages/About";
import Contact from "@/pages/Contact";
import Privacy from "@/pages/Privacy";
import Accessibility from "@/pages/Accessibility";

export default function App() {
  return (
    <Router basename={import.meta.env.BASE_URL}>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/services" element={<Services />} />
        <Route path="/services/:slug" element={<ServiceDetail />} />
        <Route path="/industries" element={<Industries />} />
        <Route path="/industries/:slug" element={<IndustryDetail />} />
        <Route path="/case-studies" element={<CaseStudies />} />
        <Route path="/case-studies/:slug" element={<CaseStudyDetail />} />
        <Route path="/insights" element={<Insights />} />
        <Route path="/insights/:slug" element={<InsightDetail />} />
        <Route path="/about" element={<About />} />
        <Route path="/contact" element={<Contact />} />
        <Route path="/privacy" element={<Privacy />} />
        <Route path="/accessibility" element={<Accessibility />} />
      </Routes>
    </Router>
  );
}
