import React, { useState, useCallback, useEffect } from 'react';
import { useSession } from '../hooks/useSession';
import { useBootstrap } from '../hooks/useBootstrap';
import { GameLayout } from '../components/layout/GameLayout';
import { StartupDossier } from '../components/startup/StartupDossier';
import { StartupCenterStage } from '../components/startup/StartupCenterStage';
import { FinancialPanel } from '../components/game/FinancialPanel';
import { AttackChoiceGrid } from '../components/game/AttackChoiceGrid';
import { RoundProgress } from '../components/game/RoundProgress';
import { RoundResultView } from '../components/game/RoundResultView';
import { SceneRenderer } from '../components/scenes/SceneRenderer';
import { FinalScene } from '../components/finals/FinalScene';
import { useGameStore } from '../stores/gameStore';
import { useAttack } from '../hooks/useAttack';
import { useRound } from '../hooks/useRound';
import { useNavigate } from 'react-router-dom';
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { api } from '../api/endpoints';
import { v4 as uuidv4 } from 'uuid';

export const GameView: React.FC = () => {
  const { session, isLoading, isFetching } = useSession();
  const { gameRules } = useBootstrap();
  const navigate = useNavigate();
  const queryClient = useQueryClient();
  const phase = useGameStore(s => s.phase);
  const setPhase = useGameStore(s => s.setPhase);
  const currentRoundId = useGameStore(s => s.currentRoundId);
  const setCurrentRoundId = useGameStore(s => s.setCurrentRoundId);
  const [showingScene, setShowingScene] = useState(false);
  const [attackError, setAttackError] = useState<string | null>(null);
  const attack = useAttack(session?.session_id || '');

  useEffect(() => {
    if (session?.status === 'result_pending' && session.current_round_id) {
      setCurrentRoundId(session.current_round_id);
      setPhase('EVENT_REVEAL');
      return;
    }
    if (session?.status === 'ready' && phase !== 'READY' && !attack.isPending && !isFetching) {
      setCurrentRoundId(null);
      setShowingScene(false);
      setPhase('READY');
    }
  }, [attack.isPending, isFetching, phase, session?.current_round_id, session?.status, setCurrentRoundId, setPhase]);

  const { data: roundResult } = useRound(currentRoundId, !!currentRoundId);
  const { data: finalResult, isLoading: isFinalLoading } = useQuery({
    queryKey: ['result', session?.session_id],
    queryFn: () => api.getResult(session!.session_id),
    enabled: session?.status === 'completed',
  });

  const continueMutation = useMutation({
    mutationFn: () => {
      if (!session || !currentRoundId) throw new Error('Отсутствует ID сессии или раунда');
      return api.continueGame(session.session_id, currentRoundId, uuidv4());
    },
    onSuccess: () => {
      setPhase('READY');
      setCurrentRoundId(null);
      queryClient.invalidateQueries({ queryKey: ['session'] });
    },
  });

  const handleSceneComplete = useCallback(() => setShowingScene(false), []);

  const handleContinueRound = () => {
    if (roundResult?.game_completed || session?.status === 'completed') {
      queryClient.invalidateQueries({ queryKey: ['session'] });
      setPhase('GAME_OVER');
    } else {
      continueMutation.mutate();
    }
  };

  const handleChoice = async (choiceId: string) => {
    setAttackError(null);
    try {
      await attack.mutateAsync(choiceId);
      setShowingScene(true);
    } catch (err: any) {
      const msg = err?.data?.error?.message || err?.data?.message || err?.message || 'Не удалось выполнить ход. Повторите попытку.';
      setAttackError(msg);
      queryClient.invalidateQueries({ queryKey: ['session'] });
    }
  };

  if (isLoading || !session) {
    return (
      <div className="min-h-screen bg-bg-primary flex items-center justify-center text-text-secondary font-mono">
        <div className="flex items-center gap-3">
          <div className="w-2.5 h-2.5 rounded-full bg-accent-lime animate-pulse" />
          <span>Загрузка данных сессии...</span>
        </div>
      </div>
    );
  }

  if (session.status === 'completed') {
    if (isFinalLoading || !finalResult) {
      return (
        <div className="min-h-screen bg-bg-primary flex flex-col items-center justify-center p-4">
          <div className="flex items-center gap-3 font-mono text-accent-lime text-sm">
            <div className="w-3 h-3 rounded-full bg-accent-lime animate-ping" />
            <span>Подведение итогов партии и подсчёт рейтинга...</span>
          </div>
        </div>
      );
    }
    return (
      <div className="min-h-screen bg-bg-primary flex flex-col items-center justify-center p-4 sm:p-8">
        <div className="max-w-2xl w-full flex flex-col gap-6">
          <FinalScene result={finalResult} />
          <button
            onClick={() => navigate('/leaderboard')}
            className="w-full py-4 px-6 bg-accent-lime text-bg-primary font-display font-bold text-sm uppercase tracking-wider rounded-xl hover:brightness-110 active:scale-[0.99] transition-all shadow-[0_0_20px_rgba(185,245,107,0.25)] flex items-center justify-center gap-2 cursor-pointer"
          >
            <span>ПЕРЕЙТИ В ЗАЛ СЛАВЫ</span><span className="font-mono text-base">→</span>
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="relative">
      {showingScene && roundResult?.event?.scene_type && (
        <SceneRenderer type={roundResult.event.scene_type} onComplete={handleSceneComplete} />
      )}
      <GameLayout
        left={<StartupDossier startup={session.startup} />}
        center={(
          <div className="flex flex-col gap-6">
            <StartupCenterStage startup={session.startup} round={session.next_round} maxRounds={gameRules?.max_rounds || 3} month={session.elapsed_months} />
            <RoundProgress round={session.next_round} maxRounds={gameRules?.max_rounds || 3} />
            {phase === 'SUBMITTING' && (
              <div role="status" className="p-6 bg-bg-card border border-border rounded-2xl flex items-center justify-center gap-3 font-mono text-sm text-text-secondary">
                <span className="w-3 h-3 rounded-full bg-accent-lime animate-pulse" />
                <span>Проводим финансовый расчёт хода...</span>
              </div>
            )}
            {phase === 'EVENT_REVEAL' && roundResult && !showingScene && (
              <RoundResultView result={roundResult} onContinue={handleContinueRound} isContinuing={continueMutation.isPending} />
            )}
            {session.can_attack && phase !== 'EVENT_REVEAL' && (
              <div className="flex-1 flex flex-col justify-end gap-3">
                {attackError && <div role="alert" className="p-3 rounded-xl bg-accent-red/10 border border-accent-red/30 text-accent-red text-xs font-mono">{attackError}</div>}
                <AttackChoiceGrid
                  choices={session.available_choices || []}
                  roundNumber={session.next_round}
                  onSelect={handleChoice}
                  disabled={phase !== 'READY' || attack.isPending}
                />
              </div>
            )}
          </div>
        )}
        right={<FinancialPanel state={session.state} />}
      />
    </div>
  );
};
