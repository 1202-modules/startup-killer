import { useQuery } from '@tanstack/react-query';
import { getLeaderboard } from '../api/endpoints';

export const useLeaderboard = () => {
  return useQuery({
    queryKey: ['leaderboard'],
    queryFn: () => getLeaderboard(25, 0),
    staleTime: 30000,
  });
};
