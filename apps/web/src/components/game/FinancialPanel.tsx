import React from 'react';
import { CashDisplay } from '../ui/CashDisplay';
import { GameState } from '../../api/types';
import { motion } from 'framer-motion';

export const FinancialPanel: React.FC<{ state: GameState }> = ({ state }) => {
  const runway = state.cash_kopeks / (state.monthly_fixed_cost_kopeks || 1);
  const runwayColor = runway < 3 ? 'text-accent-red' : runway < 6 ? 'text-accent-amber' : 'text-accent-lime';

  return (
    <div className="grid shrink-0 grid-cols-1 gap-3 rounded-xl border border-border bg-bg-card p-4 md:grid-cols-4 md:items-center md:gap-5 xl:flex xl:flex-col xl:gap-3">
      <div className="md:col-span-1 min-w-0">
        <div className="text-xs text-text-secondary font-mono mb-1">ОСТАТОК СРЕДСТВ</div>
        <div className="whitespace-nowrap font-mono text-2xl tabular-nums text-text-primary md:text-xl xl:text-2xl">
          <CashDisplay kopeks={state.cash_kopeks} />
        </div>
      </div>
      
      <div className="md:col-span-2 grid grid-cols-2 gap-4 min-w-0">
        <div>
          <div className="text-xs text-text-secondary font-mono mb-1">RUNWAY</div>
          <div className={`text-xl font-mono ${runwayColor}`}>
            {runway.toFixed(1)} мес
          </div>
        </div>
        <div>
          <div className="text-xs text-text-secondary font-mono mb-1">BURN RATE</div>
          <div className="text-sm font-mono leading-tight text-text-primary tabular-nums">
            <CashDisplay kopeks={state.monthly_fixed_cost_kopeks} className="block break-words" />
            <span className="mt-1 block text-xs text-text-secondary">/мес</span>
          </div>
        </div>
      </div>

      <div className="md:col-span-1 min-w-0">
        <div className="flex flex-wrap justify-between items-end gap-x-3 gap-y-1 mb-2">
          <div className="text-xs text-text-secondary font-mono">РЕПУТАЦИЯ</div>
          <div className="text-sm font-mono text-text-primary">{state.reputation}/100</div>
        </div>
        <div className="h-2 w-full bg-bg-surface rounded-full overflow-hidden">
          <motion.div 
            className="h-full bg-accent-lime"
            initial={{ width: 0 }}
            animate={{ width: `${state.reputation}%` }}
            transition={{ duration: 1, ease: 'easeOut' }}
          />
        </div>
      </div>
    </div>
  );
};
