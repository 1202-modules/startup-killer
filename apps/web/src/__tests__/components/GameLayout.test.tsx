import { render, screen } from '@testing-library/react';
import { describe, expect, it } from 'vitest';
import { GameLayout } from '../../components/layout/GameLayout';

describe('GameLayout', () => {
  it('keeps financial stats in a full-width top strip between tablet and desktop breakpoints', () => {
    render(
      <GameLayout
        left={<div data-testid="left" />}
        center={<div data-testid="center" />}
        right={<div data-testid="right" />}
      />,
    );

    expect(screen.getByTestId('right').parentElement).toHaveClass('md:col-span-2', 'md:row-start-1');
    expect(screen.getByTestId('left').parentElement).toHaveClass('md:row-start-2');
    expect(screen.getByTestId('center').parentElement).toHaveClass('md:row-start-2');
  });
});
