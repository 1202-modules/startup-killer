import { useMutation, useQueryClient } from '@tanstack/react-query';
import { api } from '../api/endpoints';
import { useGameStore } from '../stores/gameStore';
import { v4 as uuidv4 } from 'uuid';

export const useAttack = (sessionId: string) => {
  const setPhase = useGameStore(s => s.setPhase);
  const setCurrentRoundId = useGameStore(s => s.setCurrentRoundId);
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (choiceId: string) => api.submitChoice(sessionId, choiceId, uuidv4()),
    onMutate: () => setPhase('SUBMITTING'),
    onSuccess: result => {
      if (result.round_id) {
        setCurrentRoundId(result.round_id);
        queryClient.setQueryData(['round', result.round_id], result);
      }
      setPhase('EVENT_REVEAL');
      queryClient.invalidateQueries({ queryKey: ['session'] });
    },
    onError: () => setPhase('READY'),
  });
};
