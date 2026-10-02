import { create } from 'zustand';

export type ScenePhase =
  | 'READY'
  | 'SUBMITTING'
  | 'EVENT_REVEAL'
  | 'DEFENSE_REVEAL'
  | 'METRICS_REVEAL'
  | 'NEXT_ROUND'
  | 'GAME_OVER'
  | 'RESTORING';

interface GameState {
  phase: ScenePhase;
  setPhase: (phase: ScenePhase) => void;
  isReducedMotion: boolean;
  setReducedMotion: (val: boolean) => void;
  currentRoundId: string | null;
  setCurrentRoundId: (id: string | null) => void;
  skipAnimations: boolean;
  setSkipAnimations: (val: boolean) => void;
}

export const useGameStore = create<GameState>((set) => ({
  phase: 'READY',
  setPhase: (phase) => set({ phase }),
  isReducedMotion: typeof window !== 'undefined' ? window.matchMedia('(prefers-reduced-motion: reduce)').matches : false,
  setReducedMotion: (val) => set({ isReducedMotion: val }),
  currentRoundId: null,
  setCurrentRoundId: (currentRoundId) => set({ currentRoundId }),
  skipAnimations: false,
  setSkipAnimations: (val) => set({ skipAnimations: val }),
}));
