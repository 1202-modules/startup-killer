import { render, screen, fireEvent } from '@testing-library/react';
import { describe, it, expect, vi } from 'vitest';
import { RoundResultView } from '../../components/game/RoundResultView';
import { RoundResult } from '../../api/types';

describe('RoundResultView', () => {
  const baseResult: RoundResult = {
    status: 'success',
    round_number: 1,
    months_simulated: [1, 2, 3],
    round_id: 'round-1',
    selected_choice: { id: 'coffee-r1-a', round_number: 1, title: 'Переманить клиентов', short_description: 'Запусти конкурирующую кофейню у кампуса с более низкой ценой.', attack_narrative: 'Запусти конкурирующую кофейню у кампуса с более низкой ценой.' },
    event: {
      title: 'Университетский демпинг ударил по посещаемости',
      narrative: 'Студенты выстроились в очередь к дешёвым автоматам конкурентов, продажи CoffeeBot в кампусах упали.',
      scene_type: 'competition',
    },
    defense: {
      type: 'cost_cutting',
      summary: 'Экстренное сокращение расходов: урезаны операционные траты и бонусы команды (затраты: 2 000 000 ₽).',
      company_response: 'Операционный директор срочно меняет график точек.',
    },
    deltas: {
      cash_kopeks: -150000000,
      monthly_revenue_kopeks: -50000000,
      reputation: -12,
    },
    state_after: {
      cash_kopeks: 650000000,
      monthly_revenue_kopeks: 150000000,
      reputation: 68,
    },
    new_circumstance: 'Университеты требуют снижения арендных ставок для всех вендинговых аппаратов.',
    game_completed: false,
    next_action: 'next_round',
  };

  it('shows the selected attack and its explanation once without repeating the narrative', () => {
    render(<RoundResultView result={baseResult} onContinue={vi.fn()} />);
    expect(screen.getByText('Переманить клиентов')).toBeInTheDocument();
    expect(screen.getByText('Запусти конкурирующую кофейню у кампуса с более низкой ценой.')).toBeInTheDocument();
    expect(screen.getByText('ВАША АТАКА')).toBeInTheDocument();
    expect(screen.queryByText('Кампусный демпинг')).not.toBeInTheDocument();
    expect(screen.getAllByText('Запусти конкурирующую кофейню у кампуса с более низкой ценой.')).toHaveLength(1);
  });

  it('renders the consequence narrative without repeating the event headline', () => {
    render(<RoundResultView result={baseResult} onContinue={vi.fn()} />);
    expect(screen.queryByText(baseResult.event.title)).not.toBeInTheDocument();
    expect(screen.getByText(new RegExp(baseResult.event.narrative))).toBeInTheDocument();
  });

  it('renders localized defense title and Russian narrative summary', () => {
    render(<RoundResultView result={baseResult} onContinue={vi.fn()} />);
    expect(screen.getByText('СОКРАЩЕНИЕ РАСХОДОВ')).toBeInTheDocument();
    expect(screen.getByText(baseResult.defense.summary)).toBeInTheDocument();
    expect(screen.getByText('Операционный директор срочно меняет график точек.')).toBeInTheDocument();
  });

  it('renders financial deltas and new circumstance', () => {
    render(<RoundResultView result={baseResult} onContinue={vi.fn()} />);
    expect(screen.getByText('КАЗНА')).toBeInTheDocument();
    expect(screen.getByText('ВЫРУЧКА')).toBeInTheDocument();
    expect(screen.getByText('РЕПУТАЦИЯ')).toBeInTheDocument();
    expect(screen.getByText(baseResult.new_circumstance!)).toBeInTheDocument();
  });

  it('does not repeat a circumstance that is identical to the event narrative', () => {
    render(<RoundResultView result={{
      ...baseResult,
      new_circumstance: baseResult.event.narrative,
    }} onContinue={vi.fn()} />);
    expect(screen.getAllByText(new RegExp(baseResult.event.narrative))).toHaveLength(1);
  });

  it('renders next round button when game is not completed and triggers onContinue', () => {
    const onContinueMock = vi.fn();
    render(<RoundResultView result={baseResult} onContinue={onContinueMock} />);
    const continueBtn = screen.getByRole('button', { name: /ПЕРЕЙТИ К СЛЕДУЮЩЕМУ ХОДУ/i });
    expect(continueBtn).toBeInTheDocument();
    fireEvent.click(continueBtn);
    expect(onContinueMock).toHaveBeenCalledTimes(1);
  });

  it('renders final summary button when game is completed', () => {
    const completedResult = {
      ...baseResult,
      game_completed: true,
    };
    render(<RoundResultView result={completedResult} onContinue={vi.fn()} />);
    expect(screen.getByRole('button', { name: /УЗНАТЬ ИТОГИ ПАРТИИ/i })).toBeInTheDocument();
  });
});
