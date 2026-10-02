import { v4 as uuidv4 } from 'uuid';

let csrfToken: string | null = null;
let idempotencyKey: string | null = null;

const getHeaders = (isMutation: boolean = false) => {
  const headers: Record<string, string> = {
    'Content-Type': 'application/json',
  };
  
  if (isMutation) {
    if (csrfToken) {
      headers['X-CSRF-Token'] = csrfToken;
    }
    if (!idempotencyKey) {
      idempotencyKey = uuidv4();
    }
    headers['Idempotency-Key'] = idempotencyKey;
  }
  
  return headers;
};

export const clearIdempotencyKey = () => {
  idempotencyKey = null;
};

export const setCsrfToken = (token: string) => {
  csrfToken = token;
};

export const getCsrfToken = () => csrfToken;

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
    const headers = getHeaders(true);
    if (customIdempotencyKey) {
      headers['Idempotency-Key'] = customIdempotencyKey;
    }
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

  patch: async <T>(url: string, body?: any): Promise<T> => {
    const res = await fetch(url, {
      method: 'PATCH',
      headers: getHeaders(true),
      body: body ? JSON.stringify(body) : undefined,
      credentials: 'same-origin',
    });
    
    if (!res.ok) {
      const errorData = await res.json().catch(() => ({}));
      throw { status: res.status, data: errorData };
    }
    
    return res.json();
  },

  delete: async <T>(url: string): Promise<T> => {
    const res = await fetch(url, {
      method: 'DELETE',
      headers: getHeaders(true),
      credentials: 'same-origin',
    });
    
    if (!res.ok) {
      const errorData = await res.json().catch(() => ({}));
      throw { status: res.status, data: errorData };
    }
    
    if (res.status === 204) return undefined as T;
    return res.json();
  },
};
