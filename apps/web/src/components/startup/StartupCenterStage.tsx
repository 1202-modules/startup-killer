import React from 'react';
import { motion } from 'framer-motion';
import { StartupPublic } from '../../api/types';
import { useGameStore } from '../../stores/gameStore';

interface StartupCenterStageProps {
  startup: StartupPublic;
  round: number;
  maxRounds: number;
  month: number;
  compact?: boolean;
}

export const StartupCenterStage: React.FC<StartupCenterStageProps> = ({ startup, round, maxRounds, compact = false }) => {
  const isReducedMotion = useGameStore(s => s.isReducedMotion);
  const startMonth = Math.max(1, (round - 1) * 3 + 1);
  const endMonth = Math.min(9, round * 3);

  return (
    <motion.section
      key={round}
      initial={isReducedMotion ? false : { opacity: 0, y: 12 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3, ease: 'easeOut' }}
      className={`shrink-0 rounded-2xl border border-border bg-bg-card px-5 shadow-xl sm:px-6 ${compact ? 'py-2' : 'py-4'}`}
    >
      <div className="flex justify-end">
        <span className="rounded-lg border border-accent-lime/30 bg-bg-surface px-3 py-1.5 font-mono text-xs font-bold tracking-wider text-accent-lime">
          РАУНД {round}/{maxRounds} • МЕСЯЦ {startMonth}–{endMonth}/9
        </span>
      </div>

      <div className="mt-1 text-center">
        <p className="font-mono text-[11px] font-bold uppercase tracking-wider text-accent-lime">ЦЕЛЬ НА МУШКЕ</p>
        <h1 className="mt-1 font-display text-2xl font-extrabold uppercase tracking-tight text-text-primary sm:text-3xl">
          {startup.name}
        </h1>
        <p className="text-xs leading-relaxed text-text-secondary sm:text-sm">{startup.tagline}</p>
      </div>

      {!compact && <div className="mt-3 rounded-xl border border-border/70 bg-bg-surface/70 px-4 py-3">
        <span className="font-mono text-[10px] font-bold uppercase tracking-wider text-accent-amber">
          ЧЕМ ЗАНИМАЕТСЯ СТАРТАП
        </span>
        <p className="mt-1 text-sm leading-relaxed text-text-primary">{startup.description}</p>
      </div>}
    </motion.section>
  );
};
