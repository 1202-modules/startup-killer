import React from 'react';
import { RoundResult } from '../../api/types';
import { CashDisplay } from '../ui/CashDisplay';

interface RoundResultViewProps {
  result: RoundResult;
  onContinue: () => void;
  isContinuing?: boolean;
}

const DEFENSE_TITLES: Record<string, string> = {
  none: 'БЕЗ ЗАЩИТЫ',
  cost_cut: 'СОКРАЩЕНИЕ РАСХОДОВ',
  cost_cutting: 'СОКРАЩЕНИЕ РАСХОДОВ',
  pr: 'PR-КОНТРАТАКА',
  supplier_switch: 'СМЕНА ПОСТАВЩИКОВ',
  pivot: 'ЭКСТРЕННЫЙ ПИВОТ',
  price_war: 'ЦЕНОВАЯ ВОЙНА',
  price_cut: 'ДЕМПИНГ ЦЕН',
  legal_threat: 'ЮРИДИЧЕСКАЯ УГРОЗА',
  rebrand: 'СРОЧНЫЙ РЕБРЕНДИНГ',
  fundraise: 'ПОИСК ИНВЕСТИЦИЙ',
  product_fix: 'ТЕХНИЧЕСКИЙ ПАТЧ',
  regulatory_defense: 'ЛОББИЗМ И СУДЫ',
};

export const RoundResultView: React.FC<RoundResultViewProps> = ({
  result,
  onContinue,
  isContinuing = false,
}) => {
  const cashDelta = result.deltas.cash_kopeks;
  const revDelta = result.deltas.monthly_revenue_kopeks;
  const repDelta = result.deltas.reputation;

  const getDeltaColor = (val: number) => {
    if (val < 0) return 'text-accent-red';
    if (val > 0) return 'text-accent-lime';
    return 'text-text-secondary';
  };

  const defenseTypeNormalized = result.defense?.type ? result.defense.type.toLowerCase() : 'none';
  const defenseLabel = DEFENSE_TITLES[defenseTypeNormalized] || result.defense?.type?.toUpperCase() || 'БЕЗ ЗАЩИТЫ';

  return (
    <div className="flex flex-col gap-6 p-6 sm:p-7 bg-bg-card border border-border rounded-2xl shadow-2xl animate-in fade-in duration-300">
      {/* Header Bar */}
      <div className="flex items-center justify-between border-b border-border/60 pb-3">
        <div className="flex items-center gap-2">
          <span className="w-2.5 h-2.5 rounded-full bg-accent-lime animate-pulse" />
          <span className="font-mono text-xs uppercase tracking-wider text-accent-lime font-bold">
            ИТОГИ РАУНДА {result.round_number}
          </span>
        </div>
        <div className="font-mono text-xs text-text-secondary">
          Месяцы: {result.months_simulated?.join(', ') || 'N/A'}
        </div>
      </div>

      <div className="flex flex-col gap-3">
        <div className="flex items-center gap-2">
          <span className="font-mono text-[11px] uppercase tracking-wider text-text-secondary">
            ВАША АТАКА
          </span>
        </div>
        <div className="flex flex-col gap-2 p-4 rounded-xl bg-bg-surface/70 border border-border/50">
          {result.selected_choice && (
            <h3 className="font-display text-sm sm:text-base font-bold text-text-primary">
              {result.selected_choice.title}
            </h3>
          )}
          <p className="text-sm leading-relaxed text-text-secondary">
            {result.selected_choice?.short_description || result.event.title}
          </p>
        </div>
        <div className="flex flex-col gap-1.5">
          <span className="font-mono text-[11px] uppercase tracking-wider text-text-secondary">
            ПОСЛЕДСТВИЯ
          </span>
          <p className="text-text-secondary text-sm leading-relaxed">
            {result.event.narrative}
          </p>
        </div>
      </div>

      {result.defense.company_response && (
        <div className="flex flex-col gap-2 p-4 rounded-xl bg-accent-lime/5 border border-accent-lime/25">
          <span className="font-mono text-[11px] font-bold uppercase tracking-wider text-accent-lime">
            ОТВЕТ КОМАНДЫ СТАРТАПА
          </span>
          <p className="text-sm leading-relaxed text-text-primary">
            {result.defense.company_response}
          </p>
        </div>
      )}

      {/* Defense Maneuver */}
      <div className="flex flex-col gap-2.5 p-4 bg-bg-surface rounded-xl border border-border/70">
        <div className="flex items-center justify-between text-xs font-mono">
          <span className="text-text-secondary uppercase">ФАКТИЧЕСКИЙ ЗАЩИТНЫЙ МАНЁВР</span>
          <span className="text-accent-amber px-2.5 py-0.5 rounded bg-accent-amber/10 border border-accent-amber/25 font-bold tracking-wider">
            {defenseLabel}
          </span>
        </div>
        <p className="text-xs sm:text-sm text-text-primary leading-relaxed font-mono">
          {result.defense.summary}
        </p>
      </div>

      {/* Economic Deltas */}
      <div className="grid grid-cols-3 gap-3">
        <div className="p-3.5 rounded-xl bg-bg-surface border border-border/70 flex flex-col items-center text-center">
          <span className="text-[11px] font-mono text-text-secondary uppercase tracking-wider">
            КАЗНА
          </span>
          <span className={`font-mono text-sm sm:text-base font-bold mt-1.5 ${getDeltaColor(cashDelta)}`}>
            {cashDelta === 0 ? '0 ₽' : <CashDisplay kopeks={cashDelta} isChange />}
          </span>
        </div>
        <div className="p-3.5 rounded-xl bg-bg-surface border border-border/70 flex flex-col items-center text-center">
          <span className="text-[11px] font-mono text-text-secondary uppercase tracking-wider">
            ВЫРУЧКА
          </span>
          <span className={`font-mono text-sm sm:text-base font-bold mt-1.5 ${getDeltaColor(revDelta)}`}>
            {revDelta === 0 ? '0 ₽' : <CashDisplay kopeks={revDelta} isChange />}
          </span>
        </div>
        <div className="p-3.5 rounded-xl bg-bg-surface border border-border/70 flex flex-col items-center text-center">
          <span className="text-[11px] font-mono text-text-secondary uppercase tracking-wider">
            РЕПУТАЦИЯ
          </span>
          <span className={`font-mono text-sm sm:text-base font-bold mt-1.5 ${getDeltaColor(repDelta)}`}>
            {repDelta > 0 ? `+${repDelta}` : repDelta}
          </span>
        </div>
      </div>

      {/* New Circumstance */}
      {result.new_circumstance && result.new_circumstance !== result.event.narrative && (
        <div className="p-4 rounded-xl bg-accent-lime/5 border border-accent-lime/25 flex flex-col gap-1.5">
          <div className="flex items-center gap-2 text-accent-lime font-mono text-xs">
            <span className="w-1.5 h-1.5 rounded-full bg-accent-lime" />
            <span className="uppercase font-bold tracking-wider">НОВОЕ ОБСТОЯТЕЛЬСТВО</span>
          </div>
          <p className="text-xs sm:text-sm text-text-secondary leading-relaxed">
            {result.new_circumstance}
          </p>
        </div>
      )}

      {/* CTA Button */}
      <button
        onClick={onContinue}
        disabled={isContinuing}
        className="w-full py-4 px-6 bg-accent-lime text-bg-primary font-display font-bold text-sm uppercase tracking-wider rounded-xl hover:brightness-110 active:scale-[0.99] disabled:opacity-50 transition-all shadow-[0_0_20px_rgba(185,245,107,0.25)] flex items-center justify-center gap-2 cursor-pointer mt-1"
      >
        {isContinuing ? (
          <>
            <div className="w-4 h-4 border-2 border-bg-primary border-t-transparent rounded-full animate-spin" />
            <span>Переход к раунду...</span>
          </>
        ) : (
          <>
            <span>{result.game_completed ? 'УЗНАТЬ ИТОГИ ПАРТИИ' : 'ПЕРЕЙТИ К СЛЕДУЮЩЕМУ ХОДУ'}</span>
            <span className="font-mono text-base">→</span>
          </>
        )}
      </button>
    </div>
  );
};
