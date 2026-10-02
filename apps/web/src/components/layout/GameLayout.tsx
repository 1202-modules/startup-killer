import React from 'react';

export const GameLayout: React.FC<{
  center: React.ReactNode;
  analytics: React.ReactNode;
  dossier: React.ReactNode;
}> = ({ center, analytics, dossier }) => {
  return (
    <div className="min-h-[100dvh] bg-bg-primary p-4 text-text-primary sm:p-6 xl:h-[100dvh] xl:overflow-hidden">
      <div className="mx-auto grid max-w-[1480px] grid-cols-1 gap-4 xl:h-full xl:grid-cols-[minmax(0,1fr)_21rem]">
        <main className="flex min-w-0 flex-col gap-3 xl:min-h-0">
          {center}
        </main>
        <aside aria-label="Аналитика и досье стартапа" className="flex min-w-0 flex-col gap-3 xl:min-h-0 xl:overflow-hidden">
          {analytics}
          {dossier}
        </aside>
      </div>
    </div>
  );
};
