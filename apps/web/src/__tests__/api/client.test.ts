import { describe, it, expect, vi, beforeEach } from 'vitest';
import { apiClient, setCsrfToken, clearIdempotencyKey } from '../../api/client';
import { api } from '../../api/endpoints';

globalThis.fetch = vi.fn();

describe('apiClient', () => {
  beforeEach(() => {
    vi.resetAllMocks();
    setCsrfToken('test-csrf');
    clearIdempotencyKey();
  });

  it('adds CSRF and Idempotency-Key for POST requests', async () => {
    (globalThis.fetch as any).mockResolvedValue({
      ok: true,
      json: async () => ({ success: true })
    });

    await apiClient.post('/api/v1/test', { data: 123 });
    
    const call = (globalThis.fetch as any).mock.calls[0];
    expect(call[0]).toBe('/api/v1/test');
    expect(call[1].method).toBe('POST');
    expect(call[1].headers['X-CSRF-Token']).toBe('test-csrf');
    expect(call[1].headers['Idempotency-Key']).toBeDefined();
    expect(call[1].body).toBe(JSON.stringify({ data: 123 }));
  });

  it('does not add CSRF for GET requests', async () => {
    (globalThis.fetch as any).mockResolvedValue({
      ok: true,
      json: async () => ({ success: true })
    });

    await apiClient.get('/api/v1/test');
    
    const call = (globalThis.fetch as any).mock.calls[0];
    expect(call[0]).toBe('/api/v1/test');
    expect(call[1].method).toBe('GET');
    expect(call[1].headers['X-CSRF-Token']).toBeUndefined();
    expect(call[1].headers['Idempotency-Key']).toBeUndefined();
  });

  it('submits a catalog choice with only its id as the payload', async () => {
    (globalThis.fetch as any).mockResolvedValue({ ok: true, json: async () => ({ round_id: 'round-1' }) });
    await api.submitChoice('session-1', 'coffee-r1-a', 'key-1');
    const [, options] = (globalThis.fetch as any).mock.calls[0];
    expect(options.body).toBe(JSON.stringify({ choice_id: 'coffee-r1-a' }));
    expect(options.headers['Idempotency-Key']).toBe('key-1');
  });
});
