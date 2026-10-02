import { apiClient, setCsrfToken } from './client';
import type {
  BootstrapResponse, MySessionResponse, Session, RoundResult,
  FinalResult, LeaderboardResponse, ContinueResponse,
} from './types';

export const api = {
  bootstrap: async (): Promise<BootstrapResponse> => {
    const data = await apiClient.get<BootstrapResponse>('/api/v1/bootstrap');
    if (data?.csrf_token) setCsrfToken(data.csrf_token);
    return data;
  },
  getMySession: (): Promise<MySessionResponse> => apiClient.get('/api/v1/me/session'),
  getSession: (id: string): Promise<Session> => apiClient.get(`/api/v1/sessions/${id}`),
  createSession: (nickname: string, key: string): Promise<Session> =>
    apiClient.post('/api/v1/sessions', { nickname }, key),
  submitChoice: (sessionId: string, choiceId: string, key: string): Promise<RoundResult> =>
    apiClient.post(`/api/v1/sessions/${sessionId}/choices`, { choice_id: choiceId }, key),
  getRound: (roundId: string): Promise<RoundResult> => apiClient.get(`/api/v1/rounds/${roundId}`),
  continueGame: (sessionId: string, roundId: string, key: string): Promise<ContinueResponse> =>
    apiClient.post(`/api/v1/sessions/${sessionId}/continue`, { resolved_round_id: roundId }, key),
  getResult: (sessionId: string): Promise<FinalResult> => apiClient.get(`/api/v1/sessions/${sessionId}/result`),
  getLeaderboard: (limit?: number, offset?: number): Promise<LeaderboardResponse> =>
    apiClient.get(`/api/v1/leaderboard?limit=${limit || 25}&offset=${offset || 0}`),
};

export const getBootstrap = api.bootstrap;
export const getLeaderboard = api.getLeaderboard;
export const getRound = api.getRound;
