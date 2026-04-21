import { motion } from "framer-motion";
import { useTranslation } from 'react-i18next';

export default function HeroGraphics() {
  const { t } = useTranslation();

  return (
    <div className="relative w-full aspect-[4/3] overflow-hidden border border-border/50">
      <motion.div
        initial={{ scale: 1.05, opacity: 0 }}
        animate={{ scale: 1, opacity: 1 }}
        transition={{ duration: 1.5, ease: "easeOut" }}
        className="absolute inset-0"
      >
        <img 
          src="https://images.unsplash.com/photo-1558494949-ef010cbdcc31?q=80&w=2000&auto=format&fit=crop" 
          alt="" 
          width="800"
          height="600"
          loading="eager"
          // @ts-expect-error React 18 doesn't type fetchPriority yet
          fetchpriority="high"
          className="w-full h-full object-cover opacity-80 grayscale mix-blend-luminosity"
        />
        <div className="absolute inset-0 bg-gradient-to-t from-bg via-bg/40 to-transparent mix-blend-multiply" />
        <div className="absolute inset-0 bg-accent/5 mix-blend-overlay" />
      </motion.div>

      {/* Floating Elements */}
      <motion.div
        animate={{ y: [-10, 10, -10] }}
        transition={{ duration: 6, repeat: Infinity, ease: "easeInOut" }}
        className="absolute top-6 right-6 md:top-10 md:right-10 w-16 h-16 md:w-24 md:h-24 border border-border/50 bg-black/50 backdrop-blur-md flex items-center justify-center motion-reduce:animate-none"
      >
        <div className="w-8 h-8 md:w-12 md:h-12 border border-accent/30 border-t-accent motion-safe:animate-spin-slow" />
      </motion.div>

      <motion.div
        animate={{ y: [10, -10, 10] }}
        transition={{ duration: 8, repeat: Infinity, ease: "easeInOut", delay: 1 }}
        className="absolute bottom-6 left-6 md:bottom-16 md:left-10 w-24 h-12 md:w-32 md:h-16 border border-border/50 bg-black/50 backdrop-blur-md flex flex-col justify-center px-3 md:px-4 motion-reduce:animate-none"
      >
        <div className="text-[10px] uppercase tracking-widest text-muted font-bold">{t('misc.latency')}</div>
        <div className="text-sm font-display text-accent font-bold">12ms</div>
      </motion.div>
    </div>
  );
}
