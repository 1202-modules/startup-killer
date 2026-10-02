import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { describe, expect, it, vi } from 'vitest';
import { AttackChoiceGrid } from '../../components/game/AttackChoiceGrid';
import type { AttackChoice } from '../../api/types';

const choices: AttackChoice[] = [
  { id: 'coffee-r1-a', round_number: 1, title: 'Переманить клиентов', short_description: 'Запусти конкурирующую кофейню у кампуса с более низкой ценой.', attack_narrative: 'Запусти конкурирующую кофейню у кампуса с более низкой ценой.' },
  { id: 'coffee-r1-b', round_number: 1, title: 'Сорвать поставку', short_description: 'Добейся задержки поставки кофейных зёрен.', attack_narrative: 'Добейся задержки поставки кофейных зёрен.' },
];

describe('AttackChoiceGrid', () => {
  it('renders only choices for the active round and supports keyboard selection', async () => {
    const user = userEvent.setup();
    const onSelect = vi.fn();
    render(<AttackChoiceGrid choices={choices} roundNumber={1} onSelect={onSelect} />);
    const first = screen.getByRole('button', { name: /Переманить клиентов/ });
    expect(screen.getByText('Переманить клиентов')).toBeInTheDocument();
    expect(screen.getByText('Запусти конкурирующую кофейню у кампуса с более низкой ценой.')).toBeInTheDocument();
    expect(screen.queryByText('Кампусный демпинг')).not.toBeInTheDocument();
    expect(screen.getAllByText('Запусти конкурирующую кофейню у кампуса с более низкой ценой.')).toHaveLength(1);
    first.focus();
    await user.keyboard('{Enter}');
    expect(onSelect).toHaveBeenCalledWith('coffee-r1-a');
  });

  it('uses a single mobile column and expands to two columns', () => {
    render(<AttackChoiceGrid choices={choices} roundNumber={1} onSelect={vi.fn()} />);
    expect(screen.getByRole('group', { name: 'Выберите приём атаки' })).toHaveClass('grid-cols-1', 'sm:grid-cols-2');
  });
});
