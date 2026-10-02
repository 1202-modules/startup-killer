import React from 'react';

export const GameLayout: React.FC<{
  left: React.ReactNode;
  center: React.ReactNode;
  right: React.ReactNode;
}> = ({ left, center, right }) => {
  return (
    <div className="min-h-[100dvh] bg-bg-primary text-text-primary p-4 sm:p-6 lg:p-7">
      <div className="max-w-[1480px] mx-auto grid grid-cols-1 md:grid-cols-[260px_minmax(0,1fr)] xl:grid-cols-[320px_minmax(0,1fr)_320px] gap-6">
        <aside className="order-2 md:order-2 md:row-start-2 xl:order-1 xl:row-start-1 flex flex-col gap-6 xl:sticky xl:top-6 xl:self-start xl:max-h-[calc(100dvh-3rem)] xl:overflow-y-auto">
          {left}
        </aside>
        <main className="order-1 md:order-3 md:row-start-2 xl:order-2 xl:row-start-1 flex flex-col gap-6">
          {center}
        </main>
        <aside className="order-3 md:order-1 md:col-span-2 md:row-start-1 xl:order-3 xl:col-span-1 xl:col-start-3 xl:row-start-1 flex flex-col gap-6 xl:sticky xl:top-6 xl:self-start xl:max-h-[calc(100dvh-3rem)] xl:overflow-y-auto">
          {right}
        </aside>
      </div>
    </div>
  );
};
