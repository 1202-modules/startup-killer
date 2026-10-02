import React from 'react';
import { FinalResult } from '../../api/types';

export const Bankrupt: React.FC<{ result: FinalResult }> = ({ result }) => (
  <div className="relative min-h-[50dvh] flex flex-col items-center justify-center p-8 text-center bg-black border border-border rounded-2xl overflow-hidden">
    <div className="absolute inset-0 bg-accent-red/5 backdrop-saturate-0" />
    <h1 className="text-6xl md:text-8xl font-display font-bold text-text-primary mb-4 z-10 tracking-widest">БАНКРОТ</h1>
    <div className="text-xl md:text-2xl text-text-secondary mb-6 z-10">
      Ваш счёт: <span className="font-mono text-accent-red text-4xl block mt-2">{result.score}</span>
    </div>
    <div className="flex gap-6 mb-8 text-sm font-mono text-text-secondary z-10">
      <div>Позиция: #{result.rank} / {result.total_ranked}</div>
      <div>Выжито месяцев: {result.rounds.reduce((acc, r) => acc + (r.months_simulated?.length || 0), 0)}</div>
    </div>
    <p className="text-text-secondary max-w-lg mx-auto z-10">{result.summary}</p>
  </div>
);
