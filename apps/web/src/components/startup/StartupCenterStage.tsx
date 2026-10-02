import React from 'react';
import { motion } from 'framer-motion';
import { StartupPublic } from '../../api/types';
import { useGameStore } from '../../stores/gameStore';

interface StartupCenterStageProps {
  startup: StartupPublic;
  round: number;
  maxRounds: number;
  month: number;
}

export const StartupCenterStage: React.FC<StartupCenterStageProps> = ({
  startup,
  round,
  maxRounds,
}) => {
  const isReducedMotion = useGameStore(s => s.isReducedMotion);

  const startMonth = Math.max(1, (round - 1) * 3 + 1);
  const endMonth = Math.min(9, round * 3);
  const roundMonthBadge = `РАУНД ${round}/${maxRounds} • МЕСЯЦ ${startMonth}–${endMonth}/9`;

  return (
    <div className="bg-bg-card border border-border rounded-2xl p-5 sm:p-6 flex flex-col gap-4 shadow-xl">
      <div className="flex justify-end">
        <span className="inline-flex items-center px-3 py-1.5 rounded-xl bg-bg-surface border border-accent-lime/30 font-mono text-xs font-bold text-accent-lime tracking-wider shadow-sm">
          {roundMonthBadge}
        </span>
      </div>

      {/* Target Header Bar */}
      <div className="flex flex-col gap-1 border-b border-border/60 pb-4">
        <div className="flex items-center gap-2">
          <span className="w-2 h-2 rounded-full bg-accent-lime animate-pulse" />
          <span className="font-mono text-[11px] uppercase tracking-wider text-accent-lime font-bold">
            ЦЕЛЬ НА МУШКЕ
          </span>
        </div>
        <h1 className="text-2xl sm:text-3xl font-display font-extrabold text-text-primary uppercase tracking-tight">
          {startup.name}
        </h1>
        <p className="text-xs sm:text-sm text-text-secondary leading-relaxed">
          {startup.tagline}
        </p>
      </div>

      <div className="rounded-xl border border-border/70 bg-bg-surface/70 p-3 sm:p-4">
        <span className="font-mono text-[10px] font-bold uppercase tracking-wider text-accent-amber">
          ЧЕМ ЗАНИМАЕТСЯ СТАРТАП
        </span>
        <p className="mt-1 text-sm leading-relaxed text-text-primary max-w-none">
          {startup.description}
        </p>
      </div>

      {/* Large CGI Hero Render */}
      <div className="relative w-full rounded-2xl overflow-hidden border border-border/80 shadow-[0_0_35px_rgba(185,245,107,0.08)] bg-bg-surface max-h-[380px] aspect-[16/9] group">
        {/* Subtle Cyber Corner Crosshairs */}
        <div className="pointer-events-none absolute top-3 left-3 z-10 font-mono text-[10px] text-accent-lime/60 select-none">
          ┌ TARGET: {startup.id.toUpperCase()}
        </div>
        <div className="pointer-events-none absolute top-3 right-3 z-10 font-mono text-[10px] text-accent-lime/60 select-none">
          LIVE FEED ┐
        </div>
        <div className="pointer-events-none absolute bottom-3 left-3 z-10 font-mono text-[10px] text-accent-lime/40 select-none">
          └ SENSOR: ACTIVE
        </div>
        <div className="pointer-events-none absolute bottom-3 right-3 z-10 font-mono text-[10px] text-accent-lime/40 select-none">
          SIMULATION MODE ┘
        </div>

        {/* Responsive WebP Image */}
        <motion.picture
          initial={isReducedMotion ? false : { opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.5 }}
          className="block w-full h-full"
        >
          <source
            media="(min-width: 768px)"
            srcSet={`/assets/startups/${startup.id}/hero-desktop.webp`}
          />
          <img
            src={`/assets/startups/${startup.id}/hero-mobile.webp`}
            alt={startup.name}
            loading="eager"
            className="w-full h-full object-cover object-center group-hover:scale-[1.01] transition-transform duration-700"
          />
        </motion.picture>

        {/* Vignette Overlay */}
        <div className="pointer-events-none absolute inset-0 bg-gradient-to-t from-bg-primary/75 via-transparent to-transparent" />
      </div>
    </div>
  );
};
