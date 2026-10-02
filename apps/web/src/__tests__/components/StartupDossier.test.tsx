import { render, screen } from '@testing-library/react';
import { describe, it, expect } from 'vitest';
import { StartupDossier } from '../../components/startup/StartupDossier';
import { StartupPublic } from '../../api/types';

describe('StartupDossier', () => {
  const mockStartup: StartupPublic = {
    id: 'coffeebot',
    name: 'CoffeeBot',
    tagline: 'Кофе без бариста. Проблемы — с людьми.',
    description: 'Автоматизированные кофейни для кампусов и бизнес-центров.',
    public_facts: [
      'Большая часть точек находится в университетах.',
      'Компании нужны регулярно обслуживаемые кофемашины.',
      'Второе направление — договоры на корпоративные точки.',
    ],
    hero_asset: '/assets/startups/coffeebot-hero.webp',
  };

  it('renders dossier header and badges', () => {
    render(<StartupDossier startup={mockStartup} />);
    expect(screen.getByText('ДОСЬЕ УЯЗВИМОСТЕЙ')).toBeInTheDocument();
    expect(screen.getByText('РАЗВЕДДАННЫЕ ЦЕЛИ')).toBeInTheDocument();
  });

  it('renders industry correctly', () => {
    render(<StartupDossier startup={mockStartup} />);
    expect(screen.getByText(/Food robotics/i)).toBeInTheDocument();
  });

  it('renders custom industry if provided in startup object', () => {
    const customStartup: StartupPublic = {
      ...mockStartup,
      industry: 'Автономная робототехника',
    };
    render(<StartupDossier startup={customStartup} />);
    expect(screen.getByText('Автономная робототехника')).toBeInTheDocument();
  });

  it('renders all 3 facts with numbers and badges', () => {
    render(<StartupDossier startup={mockStartup} />);
    expect(screen.getByText('01')).toBeInTheDocument();
    expect(screen.getByText('02')).toBeInTheDocument();
    expect(screen.getByText('03')).toBeInTheDocument();

    expect(screen.getByText('Большая часть точек находится в университетах.')).toBeInTheDocument();
    expect(screen.getByText('Компании нужны регулярно обслуживаемые кофемашины.')).toBeInTheDocument();
    expect(screen.getByText('Второе направление — договоры на корпоративные точки.')).toBeInTheDocument();
  });

  it('explains how the prepared choice cards work', () => {
    render(<StartupDossier startup={mockStartup} />);
    expect(screen.getByText('КАК ВЫБРАТЬ ХОД')).toBeInTheDocument();
    expect(screen.getByText(/Выберите одну из карточек в центре/)).toBeInTheDocument();
  });
});
