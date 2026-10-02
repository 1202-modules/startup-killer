import React, { useState } from 'react';
import { useBootstrap } from '../hooks/useBootstrap';
import { useSession } from '../hooks/useSession';
import { useNavigate, Link } from 'react-router-dom';

export const WelcomeView: React.FC = () => {
  const { existingSessionId } = useBootstrap();
  const { createSession, isCreating } = useSession();
  const navigate = useNavigate();
  const [nickname, setNickname] = useState('');
  const [errorMsg, setErrorMsg] = useState<string | null>(null);

  const isValid = nickname.trim().length >= 2 && nickname.trim().length <= 24;

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (isValid && !isCreating) {
      setErrorMsg(null);
      try {
        await createSession(nickname.trim());
        navigate('/');
      } catch (err: any) {
        console.error('Error creating session', err);
        setErrorMsg(err?.response?.data?.message || 'Ошибка подключения к серверу. Попробуйте снова.');
      }
    }
  };

  const handleRestore = () => {
    navigate('/');
  };

  return (
    <div className="min-h-[100dvh] bg-bg-primary text-text-primary flex flex-col justify-between items-center p-4 sm:p-6 relative overflow-hidden">
      {/* Background cyber accent glow */}
      <div className="absolute top-[-100px] left-1/2 -translate-x-1/2 w-[600px] h-[300px] bg-accent-lime/5 blur-[120px] rounded-full pointer-events-none" />

      {/* Top Header Bar */}
      <header className="w-full max-w-4xl flex items-center justify-between py-2 z-10">
        <div className="flex items-center gap-2 font-mono text-xs text-text-secondary">
          <span className="w-2 h-2 rounded-full bg-accent-lime animate-pulse" />
          <span>СИСТЕМА САБОТАЖА v1.0</span>
        </div>
        <div className="flex items-center gap-4 text-xs font-mono">
          <Link
            to="/leaderboard"
            className="text-text-secondary hover:text-accent-lime transition-colors flex items-center gap-1.5"
          >
            <span>🏆</span>
            <span>Рейтинг</span>
          </Link>
        </div>
      </header>

      {/* Main Terminal Card */}
      <main className="max-w-lg w-full bg-bg-card/90 backdrop-blur-md border border-border p-6 sm:p-8 rounded-2xl flex flex-col gap-6 shadow-2xl z-10 my-auto">
        <div className="text-center flex flex-col items-center">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-bg-surface border border-border text-xs font-mono text-accent-lime mb-3">
            <span className="w-1.5 h-1.5 rounded-full bg-accent-lime animate-ping" />
            <span>ОПЕРАЦИЯ: ЛИКВИДАЦИЯ</span>
          </div>
          <h1 className="text-4xl sm:text-5xl font-display font-extrabold tracking-tight uppercase leading-tight mb-3">
            Убей <span className="text-accent-lime drop-shadow-[0_0_20px_rgba(185,245,107,0.35)]">Стартап</span>
          </h1>
          <p className="text-text-secondary text-sm leading-relaxed max-w-sm">
            Три раунда, чтобы обрушить экономику случайного стартапа. Выбирайте готовые атаки и смотрите, как меняются финансы компании.
          </p>
        </div>

        {/* Feature Pills */}
        <div className="grid grid-cols-3 gap-2 py-1 text-center font-mono text-[11px] text-text-secondary">
          <div className="bg-bg-surface border border-border/80 rounded-lg py-2 px-1">
            <span className="block text-accent-lime font-bold">10</span>
            <span>стартапов</span>
          </div>
          <div className="bg-bg-surface border border-border/80 rounded-lg py-2 px-1">
            <span className="block text-accent-lime font-bold">3 ХОДА</span>
            <span>по 3 месяца</span>
          </div>
          <div className="bg-bg-surface border border-border/80 rounded-lg py-2 px-1">
            <span className="block text-accent-lime font-bold">ВЫБОРЫ</span>
            <span>и экономика</span>
          </div>
        </div>

        {existingSessionId ? (
          <div className="flex flex-col gap-4 p-4 rounded-xl bg-accent-amber/10 border border-accent-amber/30">
            <div className="flex items-center gap-2 text-accent-amber font-mono text-xs">
              <span className="w-2 h-2 rounded-full bg-accent-amber animate-pulse" />
              <span>ОБНАРУЖЕНА НЕЗАВЕРШЁННАЯ СЕССИЯ</span>
            </div>
            <p className="text-xs text-text-secondary leading-relaxed">
              У вас уже есть начатая партия. Продолжите текущий ход.
            </p>
            <button
              onClick={handleRestore}
              className="w-full py-3.5 bg-accent-amber text-bg-primary font-display font-bold uppercase tracking-wider rounded-xl hover:brightness-110 active:scale-[0.99] transition-all"
            >
              Продолжить игру →
            </button>
          </div>
        ) : (
          <form onSubmit={handleSubmit} className="flex flex-col gap-5">
            <div>
              <div className="flex items-center justify-between mb-2">
                <label htmlFor="agent-nickname" className="text-xs font-mono uppercase tracking-wider text-text-secondary">
                  Позывной агента
                </label>
                <span className={`text-xs font-mono ${nickname.length >= 2 ? 'text-accent-lime' : 'text-text-secondary'}`}>
                  {nickname.length}/24
                </span>
              </div>
              <input
                id="agent-nickname"
                type="text"
                placeholder="например, ShortSqueeze"
                value={nickname}
                onChange={e => setNickname(e.target.value)}
                maxLength={24}
                autoFocus
                className="w-full px-4 py-3.5 bg-bg-surface border border-border rounded-xl text-text-primary placeholder:text-text-secondary/40 font-sans focus:outline-none focus:border-accent-lime focus:ring-1 focus:ring-accent-lime transition-all text-sm"
              />
              <p className="text-[11px] text-text-secondary/70 mt-1.5">
                Имя будет зафиксировано в едином зале славы после завершения партии.
              </p>
            </div>

            {errorMsg && (
              <div className="p-3 rounded-lg bg-accent-red/10 border border-accent-red/30 text-accent-red text-xs font-mono">
                {errorMsg}
              </div>
            )}

            <button
              type="submit"
              disabled={!isValid || isCreating}
              className="w-full py-3.5 px-6 bg-accent-lime text-bg-primary font-display font-bold text-sm uppercase tracking-wider rounded-xl transition-all duration-200 hover:brightness-110 active:scale-[0.99] disabled:opacity-40 disabled:cursor-not-allowed shadow-[0_0_20px_rgba(185,245,107,0.25)] hover:shadow-[0_0_30px_rgba(185,245,107,0.35)] flex items-center justify-center gap-2 cursor-pointer"
            >
              {isCreating ? (
                <>
                  <div className="w-4 h-4 border-2 border-bg-primary border-t-transparent rounded-full animate-spin" />
                  <span>Развёртывание цели...</span>
                </>
              ) : (
                <>
                  <span>НАЧАТЬ ОПЕРАЦИЮ</span>
                  <span className="font-mono text-base leading-none">→</span>
                </>
              )}
            </button>
          </form>
        )}
      </main>

      {/* Footer info */}
      <footer className="w-full max-w-4xl text-center py-4 text-xs font-mono text-text-secondary/50 z-10">
        «Убей стартап» • Desktop-First Сатирический Бизнес-Симулятор • 2026
      </footer>
    </div>
  );
};
