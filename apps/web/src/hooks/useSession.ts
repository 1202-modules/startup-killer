import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { api } from '../api/endpoints';
import { Session } from '../api/types';

export const useSession = () => {
  const queryClient = useQueryClient();

  const sessionQuery = useQuery<Session | null>({
    queryKey: ['session'],
    queryFn: async (): Promise<Session | null> => {
      const me = await api.getMySession();
      if (!me || !me.session_id) {
        return null;
      }
      return api.getSession(me.session_id);
    },
    retry: false,
    staleTime: 5000,
  });

  const createSessionMutation = useMutation({
    mutationFn: (nickname: string) => api.createSession(nickname, crypto.randomUUID()),
    onSuccess: (data) => {
      queryClient.setQueryData(['session'], data);
      queryClient.invalidateQueries({ queryKey: ['bootstrap'] });
    },
  });

  return {
    session: sessionQuery.data ?? null,
    isLoading: sessionQuery.isLoading,
    isFetching: sessionQuery.isFetching,
    error: sessionQuery.error,
    createSession: createSessionMutation.mutateAsync,
    isCreating: createSessionMutation.isPending,
  };
};
