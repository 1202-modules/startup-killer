import { useQuery } from '@tanstack/react-query';
import { getBootstrap } from '../api/endpoints';

export const useBootstrap = () => {
  const query = useQuery({
    queryKey: ['bootstrap'],
    queryFn: getBootstrap,
    staleTime: Infinity,
  });

  return {
    csrfToken: query.data?.csrf_token,
    existingSessionId: query.data?.existing_session_id,
    gameRules: query.data?.game_rules,
    features: query.data?.features,
    isLoading: query.isLoading,
    error: query.error,
  };
};
