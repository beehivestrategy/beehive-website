import { cn } from "@/lib/utils";
import Tag from "@/components/ui/Tag";
import { motion } from "framer-motion";

type SectionHeaderProps = {
  eyebrow?: string;
  title: string;
  description?: string;
  className?: string;
};

export default function SectionHeader({ eyebrow, title, description, className }: SectionHeaderProps) {
  return (
    <motion.div 
      initial={{ opacity: 0, y: 20 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true, margin: "-100px" }}
      transition={{ duration: 0.6 }}
      className={cn("max-w-[72ch]", className)}
    >
      {eyebrow ? (
        <div className="mb-4">
          <Tag className="bg-accent/10 border-accent/20 text-accent">{eyebrow}</Tag>
        </div>
      ) : null}
      <h2 className="font-display text-3xl tracking-tight md:text-5xl text-gradient pb-1 text-balance">{title}</h2>
      {description ? <p className="mt-4 text-base text-muted md:text-lg leading-relaxed text-pretty">{description}</p> : null}
    </motion.div>
  );
}

