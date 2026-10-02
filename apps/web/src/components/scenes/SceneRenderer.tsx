import React from 'react';
import { SceneType, RoundResult } from '../../api/types';
import { motion, AnimatePresence } from 'framer-motion';
import { useGameStore } from '../../stores/gameStore';
import { CashDisplay } from '../ui/CashDisplay';
import { STREAM_TITLES } from '../game/RoundResultView';

const GenericScene = ({ color, title, result, onComplete }: { color: string; title: string; result?: RoundResult; onComplete: () => void }) => {
  const isReduced = useGameStore(s => s.isReducedMotion);
  React.useEffect(() => {
    if (isReduced) onComplete();
    else { const t = setTimeout(onComplete, 2500); return () => clearTimeout(t); }
  }, [isReduced, onComplete]);

  return (
    <motion.div 
      initial={{ opacity: 0 }} 
      animate={{ opacity: 1 }} 
      exit={{ opacity: 0 }}
      className="absolute inset-0 z-10 flex flex-col items-center justify-center p-6 text-center backdrop-blur-sm"
      style={{ backgroundColor: `${color}40` }}
    >
      <motion.h3 
        initial={{ y: 20, opacity: 0 }}
        animate={{ y: 0, opacity: 1 }}
        className="text-3xl font-display font-bold text-white uppercase"
      >
        {title}
      </motion.h3>
      {result && <>
        <p className="mt-3 max-w-xl text-sm text-white/90">{result.event.narrative}</p>
        <div className="mt-4 flex flex-wrap justify-center gap-2 font-mono text-xs font-bold text-white">
          {Object.entries(result.impact?.affected_streams || {}).slice(0, 2).map(([stream, bps]) => (
            <span key={stream} className="rounded-lg border border-white/25 bg-black/20 px-3 py-2">
              {STREAM_TITLES[stream] || stream.replace(/_/g, ' ')} −{new Intl.NumberFormat('ru-RU', { maximumFractionDigits: 1 }).format(bps / 100)}%
            </span>
          ))}
          <span className="rounded-lg border border-white/25 bg-black/20 px-3 py-2">
            Выручка <CashDisplay kopeks={result.deltas.monthly_revenue_kopeks} isChange />/мес
          </span>
        </div>
      </>}
    </motion.div>
  );
};

export const SceneRenderer: React.FC<{ type: SceneType; result?: RoundResult; onComplete: () => void }> = ({ type, result, onComplete }) => {
  const skip = useGameStore(s => s.skipAnimations);

  React.useEffect(() => {
    if (skip) {
      onComplete();
    }
  }, [skip, onComplete]);

  if (skip) {
    return null;
  }

  const SCENE_MAP: Record<SceneType, any> = {
    competition: { color: '#F59E0B', title: 'АТАКА КОНКУРЕНТА' },
    reputation: { color: '#EF4444', title: 'РЕПУТАЦИОННЫЙ СКАНДАЛ' },
    supply: { color: '#F59E0B', title: 'СБОЙ ПОСТАВОК' },
    product: { color: '#EF4444', title: 'ТЕХНИЧЕСКИЙ СБОЙ' },
    demand: { color: '#EF4444', title: 'ПАДЕНИЕ СПРОСА' },
    cost: { color: '#B9F56B', title: 'КРИЗИС ЛИКВИДНОСТИ' },
    technology: { color: '#F59E0B', title: 'ТЕХНОЛОГИЧЕСКИЙ ТУПИК' },
    finance: { color: '#EF4444', title: 'ФИНАНСОВЫЙ КРИЗИС' },
    absurd: { color: '#B9F56B', title: 'АБСУРДНАЯ АДАПТАЦИЯ' },
  };

  const config = SCENE_MAP[type] || SCENE_MAP.finance;

  return (
    <AnimatePresence>
      <GenericScene color={config.color} title={config.title} result={result} onComplete={onComplete} />
    </AnimatePresence>
  );
};
