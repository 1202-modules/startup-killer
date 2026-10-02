import { describe, it, expect, vi, beforeEach } from 'vitest';
import { renderHook, waitFor, act } from '@testing-library/react';
import React from 'react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { useSession } from '../../hooks/useSession';
import { api } from '../../api/endpoints';

vi.mock('../../api/endpoints', () => ({
  api: {
    getMySession: vi.fn(),
    getSession: vi.fn(),
    createSession: vi.fn(),
  },
}));

describe('useSession', () => {
  let queryClient: QueryClient;

  beforeEach(() => {
    vi.clearAllMocks();
    queryClient = new QueryClient({
      defaultOptions: {
        queries: { retry: false },
      },
    });
  });

  const wrapper = ({ children }: { children: React.ReactNode }) => (
    React.createElement(QueryClientProvider, { client: queryClient }, children)
  );

  it('returns null when no active session exists', async () => {
    (api.getMySession as any).mockResolvedValueOnce({ session_id: null, status: null });

    const { result } = renderHook(() => useSession(), { wrapper });

    await waitFor(() => expect(result.current.isLoading).toBe(false));
    expect(result.current.session).toBeNull();
    expect(api.getMySession).toHaveBeenCalled();
    expect(api.getSession).not.toHaveBeenCalled();
  });

  it('reports a failed session lookup instead of treating it as no session', async () => {
    (api.getMySession as any).mockRejectedValueOnce(new Error('Server unavailable'));
    const { result } = renderHook(() => useSession(), { wrapper });
    await waitFor(() => expect(result.current.isLoading).toBe(false));
    expect(result.current.error).toBeTruthy();
  });

  it('fetches full session when session_id is returned from me/session', async () => {
    const mockSession = {
      session_id: 'sess-123',
      status: 'ready',
      next_round: 1,
      elapsed_months: 0,
      startup: { id: 'coffee', name: 'CoffeeBot' },
      state: { cash_kopeks: 1000000 },
    };

    (api.getMySession as any).mockResolvedValueOnce({ session_id: 'sess-123', status: 'ready' });
    (api.getSession as any).mockResolvedValueOnce(mockSession);

    const { result } = renderHook(() => useSession(), { wrapper });

    await waitFor(() => expect(result.current.isLoading).toBe(false));
    expect(result.current.session).toEqual(mockSession);
    expect(api.getSession).toHaveBeenCalledWith('sess-123');
  });

  it('creates a new session and updates query cache', async () => {
    (api.getMySession as any).mockResolvedValueOnce({ session_id: null, status: null });

    const newSession = {
      session_id: 'new-sess-456',
      status: 'ready',
      next_round: 1,
    };
    (api.createSession as any).mockResolvedValueOnce(newSession);

    const { result } = renderHook(() => useSession(), { wrapper });

    await waitFor(() => expect(result.current.isLoading).toBe(false));

    await act(async () => {
      await result.current.createSession('NewPlayer');
    });

    expect(api.createSession).toHaveBeenCalledWith('NewPlayer', expect.any(String));
    await waitFor(() => expect(result.current.session).toEqual(newSession));
  });
});
