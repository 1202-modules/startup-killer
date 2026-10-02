import { render, screen } from '@testing-library/react';
import { describe, it, expect, vi } from 'vitest';
import { SceneRenderer } from '../../components/scenes/SceneRenderer';

describe('SceneRenderer', () => {
  it('renders correct scene title based on type', () => {
    render(<SceneRenderer type="competition" onComplete={vi.fn()} />);
    expect(screen.getByText('АТАКА КОНКУРЕНТА')).toBeInTheDocument();
  });

  it('falls back to default if unknown type', () => {
    render(<SceneRenderer type={"unknown" as any} onComplete={vi.fn()} />);
    expect(screen.getByText('ФИНАНСОВЫЙ КРИЗИС')).toBeInTheDocument();
  });
});
