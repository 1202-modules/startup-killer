import { render } from '@testing-library/react';
import { describe, it, expect } from 'vitest';
import { StartupHero } from '../../components/startup/StartupHero';

describe('StartupHero', () => {
  it('renders picture with correct sources', () => {
    const { container } = render(<StartupHero slug="test-slug" name="Test Name" />);
    
    const source = container.querySelector('source');
    expect(source).toHaveAttribute('srcSet', '/assets/startups/test-slug/hero-desktop.webp');
    expect(source).toHaveAttribute('media', '(min-width: 768px)');
    
    const img = container.querySelector('img');
    expect(img).toHaveAttribute('src', '/assets/startups/test-slug/hero-mobile.webp');
    expect(img).toHaveAttribute('alt', 'Test Name');
    expect(img).toHaveAttribute('loading', 'eager');
  });
});
