import { render, screen } from '@testing-library/react';
import { describe, it, expect } from 'vitest';
import { FinancialPanel } from '../../components/game/FinancialPanel';

describe('FinancialPanel', () => {
  const baseState = {
    cash_kopeks: 10000000,
    monthly_revenue_kopeks: 0,
    monthly_fixed_cost_kopeks: 1000000,
    variable_cost_bps: 0,
    reputation: 80,
    active_effects_public: []
  };

  it('compresses statistics into a stable strip at tablet widths', () => {
    const { container } = render(<FinancialPanel state={baseState} />);

    expect(container.firstChild).toHaveClass('md:grid-cols-4', 'xl:flex', 'xl:flex-col');
  });

  it('calculates and displays runway correctly (> 6 months is lime)', () => {
    render(<FinancialPanel state={{ ...baseState, cash_kopeks: 10000000, monthly_fixed_cost_kopeks: 1000000 }} />);
    // Runway = 10
    expect(screen.getByText('10.0 мес')).toBeInTheDocument();
    expect(screen.getByText('10.0 мес')).toHaveClass('text-accent-lime');
  });

  it('displays amber for runway < 6 and >= 3', () => {
    render(<FinancialPanel state={{ ...baseState, cash_kopeks: 5000000, monthly_fixed_cost_kopeks: 1000000 }} />);
    // Runway = 5
    expect(screen.getByText('5.0 мес')).toBeInTheDocument();
    expect(screen.getByText('5.0 мес')).toHaveClass('text-accent-amber');
  });

  it('displays red for runway < 3', () => {
    render(<FinancialPanel state={{ ...baseState, cash_kopeks: 2000000, monthly_fixed_cost_kopeks: 1000000 }} />);
    // Runway = 2
    expect(screen.getByText('2.0 мес')).toBeInTheDocument();
    expect(screen.getByText('2.0 мес')).toHaveClass('text-accent-red');
  });
});
