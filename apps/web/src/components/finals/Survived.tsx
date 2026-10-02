import React from 'react';
import { FinalResult } from '../../api/types';
import { CashDisplay } from '../ui/CashDisplay';

export const Survived: React.FC<{ result: FinalResult }> = ({ result }) => (
  <div className="relative min-h-[50dvh] flex flex-col items-center justify-center p-8 text-center bg-accent-lime/10 border border-accent-lime/30 rounded-2xl overflow-hidden">
    <h1 className="text-5xl md:text-7xl font-display font-bold text-accent-lime mb-4">ВЫЖИЛ</h1>
    <div className="text-xl md:text-2xl text-text-primary mb-6">
      Ваш счёт: <span className="font-mono text-accent-lime text-4xl block mt-2">{result.score}</span>
    </div>
    <div className="flex gap-6 mb-8 text-sm font-mono text-text-secondary">
      <div>Позиция: #{result.rank} / {result.total_ranked}</div>
      <div>Остаток: <CashDisplay kopeks={result.final_metrics.cash_kopeks} /></div>
    </div>
    <p className="text-text-primary max-w-lg mx-auto">{result.summary}</p>
  </div>
);
