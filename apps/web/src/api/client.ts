let csrfToken: string | null = null;

const getHeaders = (idempotencyKey?: string) => {
  const headers: Record<string, string> = {
    'Content-Type': 'application/json',
  };
  
  if (idempotencyKey) {
    if (csrfToken) {
      headers['X-CSRF-Token'] = csrfToken;
    }
    headers['Idempotency-Key'] = idempotencyKey;
  }
  
  return headers;
};

export const setCsrfToken = (token: string) => {
  csrfToken = token;
};

export const apiClient = {
  get: async <T>(url: string): Promise<T> => {
    const res = await fetch(url, {
      method: 'GET',
      headers: getHeaders(),
      credentials: 'same-origin',
    });
    
    if (!res.ok) {
      const errorData = await res.json().catch(() => ({}));
      throw { status: res.status, data: errorData };
    }
    
    return res.json();
  },
  
  post: async <T>(url: string, body?: any, customIdempotencyKey?: string): Promise<T> => {
    const headers = getHeaders(customIdempotencyKey ?? crypto.randomUUID());
    const res = await fetch(url, {
      method: 'POST',
      headers,
      body: body ? JSON.stringify(body) : undefined,
      credentials: 'same-origin',
    });
    
    if (!res.ok) {
      const errorData = await res.json().catch(() => ({}));
      throw { status: res.status, data: errorData };
    }
    
    return res.json();
  },

};
