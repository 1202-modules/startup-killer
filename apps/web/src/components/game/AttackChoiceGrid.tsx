import React from 'react';
import { motion } from 'framer-motion';
import type { AttackChoice } from '../../api/types';
import { useGameStore } from '../../stores/gameStore';

interface AttackChoiceGridProps {
  choices: AttackChoice[];
  roundNumber: number;
  onSelect: (choiceId: string) => void;
  disabled?: boolean;
}

export const AttackChoiceGrid: React.FC<AttackChoiceGridProps> = ({ choices, roundNumber, onSelect, disabled = false }) => {
  const currentChoices = choices.filter(choice => choice.round_number === roundNumber);
  const isReducedMotion = useGameStore(s => s.isReducedMotion);

  return (
    <div className="flex min-h-0 flex-1 flex-col gap-3">
      <p className="shrink-0 text-sm leading-relaxed text-text-secondary">
        Выберите приём атаки. После хода увидите реакцию команды и финансовый итог.
      </p>
      <div role="group" aria-label="Выберите приём атаки" className="grid min-h-0 grid-cols-1 gap-3 sm:grid-cols-2 xl:flex-1 xl:grid-rows-2">
        {currentChoices.map((choice, index) => (
          <motion.button
            key={choice.id}
            type="button"
            disabled={disabled}
            onClick={() => onSelect(choice.id)}
            initial={isReducedMotion ? false : { opacity: 0, y: 14 }}
            animate={{ opacity: 1, y: 0 }}
            whileHover={disabled ? undefined : { y: -2 }}
            transition={{ duration: 0.24, delay: isReducedMotion ? 0 : index * 0.06 }}
            className="group flex min-h-28 flex-col rounded-xl border border-border bg-bg-card p-4 text-left transition-colors hover:border-accent-lime/70 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-accent-lime disabled:cursor-wait disabled:opacity-60 sm:p-5 xl:min-h-0"
          >
            <span className="flex items-start justify-between gap-3">
              <span className="font-display font-bold text-sm sm:text-base text-text-primary group-hover:text-accent-lime transition-colors">
                {choice.title}
              </span>
              <span aria-hidden="true" className="font-mono text-xs text-text-secondary shrink-0">{String.fromCharCode(65 + index)}</span>
            </span>
            <span className="block mt-2 text-sm leading-relaxed text-text-secondary">
              {choice.short_description}
            </span>
            {choice.combo_available && <span className="block mt-3 text-xs font-mono font-bold text-accent-lime">КОМБО ДОСТУПНО</span>}
          </motion.button>
        ))}
      </div>
    </div>
  );
};
