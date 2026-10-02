import React from 'react';
import { useLeaderboard } from '../hooks/useLeaderboard';
import { Link } from 'react-router-dom';

export const LeaderboardView: React.FC = () => {
  const { data, isLoading } = useLeaderboard();

  if (isLoading) return <div className="min-h-screen flex items-center justify-center">Загрузка...</div>;

  return (
    <div className="min-h-[100dvh] p-8 max-w-4xl mx-auto flex flex-col gap-8">
      <div className="flex justify-between items-center">
        <h1 className="text-4xl font-display font-bold text-text-primary">Таблица лидеров</h1>
        <Link to="/home" className="text-accent-lime hover:underline font-mono text-sm">На главную</Link>
      </div>

      <div className="bg-bg-card border border-border rounded-xl overflow-hidden">
        <table className="w-full text-left">
          <thead className="bg-bg-surface text-xs font-mono text-text-secondary uppercase">
            <tr>
              <th className="p-4">Место</th>
              <th className="p-4">Игрок</th>
              <th className="p-4">Стартап</th>
              <th className="p-4 text-right">Очки</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-border">
            {data?.items.map((item: any) => (
              <tr key={`${item.rank}-${item.nickname}`} className={item.is_me ? 'bg-accent-lime/5' : ''}>
                <td className="p-4 font-mono font-bold text-text-secondary">#{item.rank}</td>
                <td className={`p-4 font-bold ${item.is_me ? 'text-accent-lime' : 'text-text-primary'}`}>
                  {item.nickname}
                </td>
                <td className="p-4 text-text-secondary text-sm">{item.startup_name}</td>
                <td className="p-4 text-right font-mono text-accent-lime font-bold">{item.score}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};
