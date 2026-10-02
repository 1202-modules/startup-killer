import React from 'react';
import { fireEvent, render, screen, waitFor } from '@testing-library/react';
import { beforeEach, describe, expect, it, vi } from 'vitest';
import { GameView } from '../../views/GameView';
import { useGameStore } from '../../stores/gameStore';

const { mutateAsync } = vi.hoisted(() => ({ mutateAsync: vi.fn() }));

vi.mock('../../hooks/useSession', () => ({
  useSession: () => ({ session: {
    session_id: 'session-1', status: 'ready', can_attack: true, can_continue: false,
    next_round: 1, elapsed_months: 0,
    startup: { id: 'coffeebot', name: 'CoffeeBot', public_facts: [] },
    state: { cash_kopeks: 0, monthly_fixed_cost_kopeks: 1 },
    available_choices: [{ id: 'coffee-r1-a', round_number: 1, title: 'Переманить клиентов', short_description: 'Запусти конкурирующую кофейню у кампуса с более низкой ценой.', attack_narrative: 'Запусти конкурирующую кофейню у кампуса с более низкой ценой.' }],
  }, isLoading: false, isFetching: false }),
}));
vi.mock('../../hooks/useBootstrap', () => ({ useBootstrap: () => ({ gameRules: { max_rounds: 3 } }) }));
vi.mock('../../hooks/useAttack', () => ({ useAttack: () => ({ mutateAsync, isPending: false }) }));
vi.mock('../../hooks/useRound', () => ({ useRound: () => ({ data: undefined }) }));
vi.mock('react-router-dom', () => ({ useNavigate: () => vi.fn() }));
vi.mock('@tanstack/react-query', () => ({
  useQueryClient: () => ({ invalidateQueries: vi.fn(), setQueryData: vi.fn() }),
  useMutation: () => ({ mutate: vi.fn(), isPending: false }),
  useQuery: () => ({ data: undefined, isLoading: false }),
}));
vi.mock('../../components/layout/GameLayout', () => ({ GameLayout: ({ center }: { center: React.ReactNode }) => <div>{center}</div> }));
vi.mock('../../components/startup/StartupDossier', () => ({ StartupDossier: () => null }));
vi.mock('../../components/startup/StartupCenterStage', () => ({ StartupCenterStage: () => null }));
vi.mock('../../components/game/FinancialPanel', () => ({ FinancialPanel: () => null }));
vi.mock('../../components/game/RoundProgress', () => ({ RoundProgress: () => null }));
vi.mock('../../components/game/RoundResultView', () => ({ RoundResultView: () => null }));
vi.mock('../../components/scenes/SceneRenderer', () => ({ SceneRenderer: () => null }));
vi.mock('../../components/finals/FinalScene', () => ({ FinalScene: () => null }));

describe('GameView', () => {
  beforeEach(() => {
    mutateAsync.mockReset();
    useGameStore.setState({ phase: 'READY', currentRoundId: null });
  });

  it('renders current round cards and sends only the selected choice id', async () => {
    render(<GameView />);
    expect(screen.getByRole('button', { name: /Переманить клиентов/ })).toBeInTheDocument();
    fireEvent.click(screen.getByRole('button', { name: /Переманить клиентов/ }));
    await waitFor(() => expect(mutateAsync).toHaveBeenCalledWith('coffee-r1-a'));
  });
});
