import React from 'react';
import { FinalResult } from '../../api/types';
import { Survived } from './Survived';
import { DeepCrisis } from './DeepCrisis';
import { NearBankruptcy } from './NearBankruptcy';
import { Bankrupt } from './Bankrupt';

export const FinalScene: React.FC<{ result: FinalResult }> = ({ result }) => {
  switch (result.final_status) {
    case 'survived': return <Survived result={result} />;
    case 'deep_crisis': return <DeepCrisis result={result} />;
    case 'near_bankruptcy': return <NearBankruptcy result={result} />;
    case 'bankrupt': return <Bankrupt result={result} />;
    default: return <Bankrupt result={result} />;
  }
};
