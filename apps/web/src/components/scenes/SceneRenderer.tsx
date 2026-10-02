import React from 'react';
import { SceneType } from '../../api/types';
import { motion, AnimatePresence } from 'framer-motion';
import { useGameStore } from '../../stores/gameStore';

const GenericScene = ({ color, title, onComplete }: any) => {
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
    </motion.div>
  );
};

export const SceneRenderer: React.FC<{ type: SceneType; onComplete: () => void }> = ({ type, onComplete }) => {
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
      <GenericScene color={config.color} title={config.title} onComplete={onComplete} />
    </AnimatePresence>
  );
};
