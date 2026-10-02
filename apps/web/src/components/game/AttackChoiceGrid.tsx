import React from 'react';
import { motion } from 'framer-motion';
import type { AttackChoice } from '../../api/types';

interface AttackChoiceGridProps {
  choices: AttackChoice[];
  roundNumber: number;
  onSelect: (choiceId: string) => void;
  disabled?: boolean;
}

export const AttackChoiceGrid: React.FC<AttackChoiceGridProps> = ({ choices, roundNumber, onSelect, disabled = false }) => {
  const currentChoices = choices.filter(choice => choice.round_number === roundNumber);

  return (
    <div className="flex flex-col gap-3">
      <p className="text-sm leading-relaxed text-text-secondary">
        Выберите приём атаки. Заголовок называет способ, описание показывает, как он ударит по бизнесу. После хода увидите реакцию команды, фактическую защиту (иногда её не будет) и финансовый итог за три месяца.
      </p>
      <div role="group" aria-label="Выберите приём атаки" className="grid grid-cols-1 sm:grid-cols-2 gap-3">
        {currentChoices.map((choice, index) => (
          <motion.button
            key={choice.id}
            type="button"
            disabled={disabled}
            onClick={() => onSelect(choice.id)}
            whileHover={disabled ? undefined : { y: -2 }}
            transition={{ duration: 0.16 }}
            className="group min-h-28 p-4 sm:p-5 text-left bg-bg-card border border-border rounded-xl hover:border-accent-lime/70 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-accent-lime disabled:opacity-60 disabled:cursor-wait transition-colors"
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
          </motion.button>
        ))}
      </div>
    </div>
  );
};
