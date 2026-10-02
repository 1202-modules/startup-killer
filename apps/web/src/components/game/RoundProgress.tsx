import React from 'react';
import { useGameStore } from '../../stores/gameStore';

export const RoundProgress: React.FC<{ round: number; maxRounds: number }> = ({ round, maxRounds }) => {
  const phase = useGameStore(s => s.phase);
  const isBlinking = phase === 'SUBMITTING';
  
  return (
    <div className="flex gap-2 items-center">
      {Array.from({ length: maxRounds }).map((_, i) => (
        <div 
          key={i} 
          className={`h-2 flex-1 rounded-full ${i < round ? 'bg-accent-lime' : 'bg-bg-surface'} 
          ${isBlinking && i === round - 1 ? 'animate-pulse' : ''}`} 
        />
      ))}
    </div>
  );
};
