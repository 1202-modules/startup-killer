import React from 'react';
import { StartupPublic } from '../../api/types';

const INDUSTRY_BY_SLUG: Record<string, string> = {
  coffeebot: 'Food robotics',
  petmind: 'Pet AI',
  foodrover: 'Delivery robotics',
  studygenie: 'EdTech AI',
  sleepwork: 'Office wellness',
  fitmirror: 'Fitness hardware',
  cloudkitchen: 'Food delivery',
  agrodrone: 'AgriTech',
  moodads: 'AdTech',
  renteverything: 'Rental marketplace',
};

const FACT_TAGS: string[] = [
  'КЛИЕНТСКИЙ СЕГМЕНТ',
  'ОПЕРАЦИОННАЯ МОДЕЛЬ',
  'ИСТОЧНИК ВЫРУЧКИ',
];

interface StartupDossierProps {
  startup: StartupPublic;
}

export const StartupDossier: React.FC<StartupDossierProps> = ({ startup }) => {
  const industry = startup.industry || INDUSTRY_BY_SLUG[startup.id] || 'Технологический сектор';

  return (
    <div className="flex flex-col gap-3 rounded-2xl border border-border bg-bg-card p-4 shadow-lg xl:min-h-0 xl:flex-1">
      {/* Dossier Header */}
      <div className="flex flex-col gap-1 border-b border-border/60 pb-3">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <span className="w-2 h-2 rounded-full bg-accent-lime animate-pulse" />
            <span className="font-mono text-[11px] uppercase tracking-wider text-accent-lime font-bold">
              РАЗВЕДДАННЫЕ ЦЕЛИ
            </span>
          </div>
          <span className="font-mono text-[10px] text-text-secondary uppercase px-2 py-0.5 rounded bg-bg-surface border border-border">
            ID: {startup.id}
          </span>
        </div>

        <h2 className="mt-1 font-display text-xl font-black uppercase tracking-tight text-text-primary">
          ДОСЬЕ УЯЗВИМОСТЕЙ
        </h2>

        <div className="flex items-center gap-2 mt-1">
          <span className="text-[11px] font-mono text-text-secondary uppercase">Отрасль:</span>
          <span className="text-xs font-mono font-semibold text-accent-amber px-2 py-0.5 rounded bg-accent-amber/10 border border-accent-amber/20">
            {industry}
          </span>
        </div>
      </div>

      {/* Facts List (01, 02, 03) */}
      <div className="flex flex-col gap-2">
        <div className="flex items-center justify-between text-[11px] font-mono text-text-secondary uppercase tracking-wider">
          <span>КЛЮЧЕВЫЕ ФАКТЫ О ЦЕЛИ</span>
          <span className="text-accent-lime/70">{startup.public_facts.length} / 03</span>
        </div>

        {startup.public_facts.map((fact, index) => {
          const num = (index + 1).toString().padStart(2, '0');
          const tag = FACT_TAGS[index] || `ФАКТ ${num}`;

          return (
            <div
              key={index}
              className="group flex flex-col gap-1.5 rounded-xl border border-border/80 bg-bg-surface/80 p-2.5 transition-colors hover:border-accent-lime/40"
            >
              <div className="flex items-center justify-between">
                <span className="font-mono text-xs font-bold text-accent-lime group-hover:text-accent-lime transition-colors">
                  {num}
                </span>
                <span className="font-mono text-[9px] uppercase tracking-wider text-text-secondary px-1.5 py-0.5 rounded bg-bg-primary/60 border border-border/60">
                  {tag}
                </span>
              </div>
              <p className="text-xs leading-snug text-text-primary">
                {fact}
              </p>
            </div>
          );
        })}
      </div>

      {/* Choice Guidance */}
      <div className="flex flex-col gap-2 rounded-xl border border-accent-amber/25 bg-accent-amber/5 p-3 xl:hidden">
        <div className="flex items-center gap-2 text-accent-amber font-mono text-xs font-bold uppercase tracking-wider">
          <span>КАК ВЫБРАТЬ ХОД</span>
        </div>
        <p className="text-[11px] font-mono text-text-secondary leading-relaxed">
          Выберите одну из карточек в центре. Варианты связаны с фактами и бизнес-моделью этой компании.
        </p>
      </div>
    </div>
  );
};
