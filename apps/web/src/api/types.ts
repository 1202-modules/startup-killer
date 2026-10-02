export type SessionStatus = 'ready' | 'result_pending' | 'completed';
export type SceneType = 'competition' | 'reputation' | 'supply' | 'product' | 'demand' | 'cost' | 'technology' | 'finance' | 'absurd';
export type FinalStatus = 'survived' | 'deep_crisis' | 'near_bankruptcy' | 'bankrupt';

export interface BootstrapResponse {
  csrf_token: string;
  existing_session_id: string | null;
  game_rules: { max_rounds: number; months_per_round: number; one_attempt_per_browser: boolean; };
  features: { sound_default: boolean; };
}

export interface MySessionResponse {
  session_id: string | null;
  status?: SessionStatus;
}

export interface AttackChoice {
  id: string;
  round_number: number;
  title: string;
  short_description: string;
  attack_narrative: string;
}

export interface StartupPublic {
  id: string;
  name: string;
  tagline: string;
  description: string;
  public_facts: string[];
  hero_asset: string;
  industry?: string;
}

export interface ActiveEffect {
  id: string;
  description: string;
}

export interface GameState {
  cash_kopeks: number;
  monthly_revenue_kopeks: number;
  monthly_fixed_cost_kopeks: number;
  variable_cost_bps: number;
  reputation: number;
  active_effects_public: string[];
}

export interface Session {
  session_id: string;
  status: SessionStatus;
  next_round: number;
  elapsed_months: number;
  startup: StartupPublic;
  state: GameState;
  rounds?: any[];
  current_round_id: string | null;
  available_choices: AttackChoice[];
  can_attack: boolean;
  can_continue: boolean;
  completed: boolean;
  ranking_eligible?: boolean;
}

export interface RoundResult {
  status: string;
  round_id: string;
  round_number: number;
  selected_choice?: AttackChoice | null;
  months_simulated: number[];
  event: { title: string; narrative: string; scene_type: SceneType; };
  defense: { type: string; summary: string; company_response?: string | null; };
  deltas: { cash_kopeks: number; monthly_revenue_kopeks: number; reputation: number; };
  state_after: { cash_kopeks: number; monthly_revenue_kopeks: number; reputation: number; };
  new_circumstance?: string | null;
  game_completed: boolean;
  next_action: string;
}

export interface ContinueResponse {
  session_id: string;
  status: string;
  next_round: number;
}

export interface FinalMetrics {
  cash_kopeks: number;
  runway_months: number;
}

export interface FinalResult {
  session_id: string;
  final_status: FinalStatus;
  score: number;
  rank: number;
  total_ranked: number;
  startup: { id: string; name: string };
  final_metrics: FinalMetrics;
  score_breakdown: Record<string, number>;
  rounds: any[];
  summary: string;
}

export interface LeaderboardEntry {
  rank: number;
  nickname: string;
  startup_name: string;
  startup_slug?: string;
  score: number;
  final_status: FinalStatus;
  completed_at: string;
  is_me?: boolean;
  is_current_player?: boolean;
}

export interface LeaderboardResponse {
  total: number;
  items: LeaderboardEntry[];
  my_entry: LeaderboardEntry | null;
}
