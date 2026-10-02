import React from 'react';

interface CashDisplayProps {
  kopeks: number;
  className?: string;
  isChange?: boolean;
}

export const CashDisplay: React.FC<CashDisplayProps> = ({ kopeks, className = '', isChange = false }) => {
  const rubles = Math.abs(kopeks) / 100;
  
  const formatted = new Intl.NumberFormat('ru-RU', {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  }).format(rubles);

  const sign = kopeks < 0 ? '-' : (isChange && kopeks > 0 ? '+' : '');
  const displayString = `${sign}${formatted} ₽`;

  return (
    <span className={`font-mono ${className}`}>
      {displayString}
    </span>
  );
};
