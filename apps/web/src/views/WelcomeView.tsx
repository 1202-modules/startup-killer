import React, { useState } from 'react';
import { useBootstrap } from '../hooks/useBootstrap';
import { useSession } from '../hooks/useSession';
import { useNavigate, Link } from 'react-router-dom';

export const WelcomeView: React.FC = () => {
  const { existingSessionId } = useBootstrap();
  const { createSession, isCreating, session } = useSession();
  const navigate = useNavigate();
  const [nickname, setNickname] = useState('');
  const [errorMsg, setErrorMsg] = useState<string | null>(null);
  const [showTelegramGate, setShowTelegramGate] = useState(true);

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
        setErrorMsg(err?.data?.error?.message || 'Ошибка подключения к серверу. Попробуйте снова.');
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
        {!showTelegramGate && (
          <Link
            to="/leaderboard"
            className="text-xs font-mono text-text-secondary hover:text-accent-lime transition-colors flex items-center gap-1.5"
          >
            <span>🏆</span>
            <span>Рейтинг</span>
          </Link>
        )}
      </header>

      {showTelegramGate ? (
        <main className="relative isolate max-w-lg w-full overflow-hidden bg-bg-card border border-border rounded-2xl shadow-2xl z-10 my-auto">
          <div aria-hidden="true" className="pointer-events-none absolute inset-0 overflow-hidden">
            <span className="absolute -top-14 -left-12 h-36 w-44 rounded-[2rem] bg-gradient-to-br from-[#ffd6b5] via-[#f47a3c] to-[#d84d1e] opacity-90" />
            <span className="absolute -top-16 -right-10 h-36 w-40 rounded-[2rem] bg-gradient-to-br from-[#ffb17e] via-[#ec6930] to-[#bd3f18] opacity-90" />
            <span className="absolute -bottom-20 -left-12 h-36 w-44 rounded-[2rem] bg-gradient-to-br from-[#ef6b31] via-[#e86a32] to-[#ffd2ad] opacity-90" />
            <span className="absolute -bottom-20 -right-14 h-36 w-48 rounded-[2rem] bg-gradient-to-br from-[#d94d1e] via-[#ef793e] to-[#ffd8bc] opacity-90" />
          </div>
          <div className="relative m-3 sm:m-4 rounded-xl bg-bg-primary/95 px-5 py-7 sm:px-8 sm:py-8 text-center flex flex-col items-center gap-5">
            <div>
              <p className="text-xs font-mono uppercase tracking-[0.18em] text-[#f38a56] mb-3">Связь с операционным штабом</p>
              <h1 className="text-3xl sm:text-4xl font-display font-extrabold tracking-tight text-text-primary">Сначала — Telegram</h1>
              <p className="mt-3 max-w-sm text-sm leading-relaxed text-text-secondary">
                Отсканируйте QR-код, чтобы открыть бота. Когда будете готовы, нажмите «Продолжить».
              </p>
            </div>

            <div className="rounded-[1.35rem] bg-white p-3 shadow-[0_0_34px_rgba(239,103,48,0.24)]">
              <img
                src="/assets/telegram/platypus-bot-qr.png"
                alt="QR-код для открытия Telegram-бота platypusorder_bot"
                width="430"
                height="430"
                className="block h-60 w-60 sm:h-64 sm:w-64"
              />
            </div>

            <button
              type="button"
              onClick={() => setShowTelegramGate(false)}
              className="w-full rounded-xl bg-[#f07a3f] px-6 py-3.5 font-display text-sm font-bold uppercase tracking-wider text-[#171411] transition-all duration-200 hover:brightness-110 active:scale-[0.99] focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-4 focus-visible:outline-[#ffc09b]"
            >
              Продолжить <span aria-hidden="true" className="ml-1">→</span>
            </button>
          </div>
        </main>
      ) : (
      /* Main Terminal Card */
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

        {existingSessionId && session?.status !== 'completed' ? (
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
              <textarea
                id="agent-nickname"
                placeholder="например, ShortSqueeze"
                value={nickname}
                onChange={e => setNickname(e.target.value)}
                maxLength={24}
                rows={1}
                autoFocus
                className="w-full resize-none px-4 py-3.5 bg-bg-surface border border-border rounded-xl text-text-primary placeholder:text-text-secondary/40 font-sans focus:outline-none focus:border-accent-lime focus:ring-1 focus:ring-accent-lime transition-all text-sm"
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
      )}

      {/* Footer info */}
      <footer className="w-full max-w-4xl text-center py-4 text-xs font-mono text-text-secondary/50 z-10">
        «Убей стартап» • Desktop-First Сатирический Бизнес-Симулятор • 2026
      </footer>
    </div>
  );
};
