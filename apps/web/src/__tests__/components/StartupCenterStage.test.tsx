import { render, screen } from '@testing-library/react';
import { describe, it, expect } from 'vitest';
import { StartupCenterStage } from '../../components/startup/StartupCenterStage';
import { StartupPublic } from '../../api/types';

describe('StartupCenterStage', () => {
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

  it('renders target name, tagline, and round/month badge', () => {
    render(
      <StartupCenterStage
        startup={mockStartup}
        round={1}
        maxRounds={3}
        month={1}
      />
    );

    expect(screen.getByText('CoffeeBot')).toBeInTheDocument();
    expect(screen.getByText('Кофе без бариста. Проблемы — с людьми.')).toBeInTheDocument();
    expect(screen.getByText('ЧЕМ ЗАНИМАЕТСЯ СТАРТАП')).toBeInTheDocument();
    expect(screen.getByText('Автоматизированные кофейни для кампусов и бизнес-центров.')).toBeInTheDocument();
    expect(screen.getByText(/РАУНД 1\/3 • МЕСЯЦ 1–3\/9/i)).toBeInTheDocument();
  });

  it('renders responsive WebP hero sources and image', () => {
    const { container } = render(
      <StartupCenterStage
        startup={mockStartup}
        round={2}
        maxRounds={3}
        month={4}
      />
    );

    const source = container.querySelector('source');
    expect(source).toHaveAttribute('srcSet', '/assets/startups/coffeebot/hero-desktop.webp');
    expect(source).toHaveAttribute('media', '(min-width: 768px)');

    const img = container.querySelector('img');
    expect(img).toHaveAttribute('src', '/assets/startups/coffeebot/hero-mobile.webp');
    expect(img).toHaveAttribute('alt', 'CoffeeBot');
  });
});
