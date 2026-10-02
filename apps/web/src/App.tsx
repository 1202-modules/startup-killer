import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { WelcomeView } from './views/WelcomeView';
import { GameView } from './views/GameView';
import { LeaderboardView } from './views/LeaderboardView';
import { useBootstrap } from './hooks/useBootstrap';
import { useSession } from './hooks/useSession';

const RootGuard = () => {
  const { existingSessionId, isLoading: bootLoading } = useBootstrap();
  const { session, isLoading: sessionLoading } = useSession();

  if (bootLoading || (existingSessionId && sessionLoading)) {
    return (
      <div className="min-h-screen bg-bg-primary flex items-center justify-center text-text-secondary font-mono">
        <div className="flex items-center gap-3">
          <div className="w-2.5 h-2.5 rounded-full bg-accent-lime animate-pulse" />
          <span>Инициализация терминала...</span>
        </div>
      </div>
    );
  }

  if (session) {
    return <GameView />;
  }

  return <WelcomeView />;
};

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<RootGuard />} />
        <Route path="/home" element={<WelcomeView />} />
        <Route path="/leaderboard" element={<LeaderboardView />} />
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
