
import { render, screen } from '@testing-library/react';
import { describe, it, expect } from 'vitest';
import { CashDisplay } from '../../components/ui/CashDisplay';

describe('CashDisplay', () => {
  it('formats normal positive kopeks correctly', () => {
    render(<CashDisplay kopeks={1234567890} />);
    // 12345678.90 -> 12 345 678,90 ₽
    const display = screen.getByText(/12\s?345\s?678,90\s?₽/);
    expect(display).toBeInTheDocument();
  });

  it('formats exact millions correctly', () => {
    render(<CashDisplay kopeks={800000000} />);
    // 8000000.00 -> 8 000 000,00 ₽
    const display = screen.getByText(/8\s?000\s?000,00\s?₽/);
    expect(display).toBeInTheDocument();
  });

  it('formats zero correctly', () => {
    render(<CashDisplay kopeks={0} />);
    const display = screen.getByText(/0,00\s?₽/);
    expect(display).toBeInTheDocument();
  });

  it('formats negative kopeks correctly', () => {
    render(<CashDisplay kopeks={-162000000} />);
    // -1620000.00 -> -1 620 000,00 ₽
    const display = screen.getByText(/-1\s?620\s?000,00\s?₽/);
    expect(display).toBeInTheDocument();
  });

  it('adds plus sign if isChange is true and value is positive', () => {
    render(<CashDisplay kopeks={10000} isChange={true} />);
    const display = screen.getByText(/\+100,00\s?₽/);
    expect(display).toBeInTheDocument();
  });
});
