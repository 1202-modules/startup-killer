import React from 'react';
import { CashDisplay } from '../ui/CashDisplay';
import { GameState } from '../../api/types';
import { motion } from 'framer-motion';

export const FinancialPanel: React.FC<{ state: GameState }> = ({ state }) => {
  const runway = state.cash_kopeks / (state.monthly_fixed_cost_kopeks || 1);
  const runwayColor = runway < 3 ? 'text-accent-red' : runway < 6 ? 'text-accent-amber' : 'text-accent-lime';

  return (
    <div className="bg-bg-card border border-border rounded-xl p-5 grid grid-cols-1 gap-4 md:grid-cols-4 md:items-center md:gap-5 xl:flex xl:flex-col xl:gap-6">
      <div className="md:col-span-1">
        <div className="text-xs text-text-secondary font-mono mb-1">ОСТАТОК СРЕДСТВ</div>
        <div className="text-2xl md:text-xl xl:text-3xl font-mono text-text-primary">
          <CashDisplay kopeks={state.cash_kopeks} />
        </div>
      </div>
      
      <div className="md:col-span-2 grid grid-cols-2 gap-4">
        <div>
          <div className="text-xs text-text-secondary font-mono mb-1">RUNWAY</div>
          <div className={`text-xl font-mono ${runwayColor}`}>
            {runway.toFixed(1)} мес
          </div>
        </div>
        <div>
          <div className="text-xs text-text-secondary font-mono mb-1">BURN RATE</div>
          <div className="text-sm font-mono text-text-primary">
            <CashDisplay kopeks={state.monthly_fixed_cost_kopeks} /> /мес
          </div>
        </div>
      </div>

      <div className="md:col-span-1">
        <div className="flex justify-between items-end mb-2">
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
