import { render, screen } from '@testing-library/react';
import { describe, expect, it } from 'vitest';
import { GameLayout } from '../../components/layout/GameLayout';

describe('GameLayout', () => {
  it('keeps analytics and dossier together on the right of the game stage', () => {
    const { container } = render(
      <GameLayout
        center={<div data-testid="center" />}
        analytics={<div data-testid="analytics" />}
        dossier={<div data-testid="dossier" />}
      />,
    );

    expect(screen.getByTestId('center').closest('main')).toBeInTheDocument();
    expect(screen.getByTestId('analytics').closest('aside')).toBe(screen.getByTestId('dossier').closest('aside'));
    expect(container.firstChild).toHaveClass('xl:h-[100dvh]', 'xl:overflow-hidden');
  });
});
