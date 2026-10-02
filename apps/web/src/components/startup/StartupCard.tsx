import React from 'react';
import { StartupPublic } from '../../api/types';
import { StartupHero } from './StartupHero';

export const StartupCard: React.FC<{ startup: StartupPublic; round: number; maxRounds: number; month: number }> = ({ startup, round, maxRounds, month }) => {
  return (
    <div className="bg-bg-card border border-border rounded-xl p-4 flex flex-col gap-4">
      <div className="flex justify-between text-xs text-text-secondary font-mono tracking-wider">
        <span>РАУНД {round}/{maxRounds}</span>
        <span>МЕСЯЦ {month}/9</span>
      </div>
      <StartupHero slug={startup.id} name={startup.name} />
      <div>
        <h2 className="text-2xl font-display text-text-primary mb-1">{startup.name}</h2>
        <p className="text-sm text-text-secondary">{startup.tagline}</p>
      </div>
      <div className="flex flex-col gap-2 mt-2">
        {startup.public_facts.map((fact, i) => (
          <div key={i} className="bg-bg-surface px-3 py-2 rounded-lg text-sm text-text-primary border border-border flex gap-3 items-start">
            <span className="text-accent-lime font-mono text-xs opacity-50 mt-0.5">{(i+1).toString().padStart(2, '0')}</span>
            <span>{fact}</span>
          </div>
        ))}
      </div>
    </div>
  );
};
