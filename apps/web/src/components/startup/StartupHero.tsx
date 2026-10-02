import React from 'react';
import { motion } from 'framer-motion';
import { useGameStore } from '../../stores/gameStore';

export const StartupHero: React.FC<{ slug: string; name: string }> = ({ slug, name }) => {
  const isReducedMotion = useGameStore(s => s.isReducedMotion);
  return (
    <motion.picture 
      initial={isReducedMotion ? false : { opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 0.5 }}
      className="block w-full rounded-xl overflow-hidden aspect-[4/5] md:aspect-[16/10] bg-bg-surface"
    >
      <source media="(min-width: 768px)" srcSet={`/assets/startups/${slug}/hero-desktop.webp`} />
      <img 
        src={`/assets/startups/${slug}/hero-mobile.webp`} 
        alt={name} 
        loading="eager" 
        className="w-full h-full object-cover object-center"
      />
    </motion.picture>
  );
};
