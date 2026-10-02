import { useQuery } from '@tanstack/react-query';
import { getRound } from '../api/endpoints';

export const useRound = (roundId: string | null, enabled: boolean) => {
  return useQuery({
    queryKey: ['round', roundId],
    queryFn: () => getRound(roundId!),
    enabled: !!roundId && enabled,
    staleTime: Infinity,
  });
};
