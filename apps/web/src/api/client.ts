import axios from 'axios';

const baseURL = process.env.NEXT_PUBLIC_API_URL ||
  (typeof window !== 'undefined' ? `http://${window.location.hostname}:8000/api/v1` : 'http://localhost:8000/api/v1');

export const apiClient = axios.create({
  baseURL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export interface ChatResponse {
  response: string;
}

export interface SearchResult {
  content: string;
  metadata: {
    source: string;
    filename: string;
    type: string;
  };
}

export interface SearchResponse {
  results: SearchResult[];
}

export const chatApi = {
  sendMessage: async (message: string) => {
    const response = await apiClient.post<ChatResponse>('/chat', { message });
    return response.data;
  },
  search: async (query: string) => {
    const response = await apiClient.post<SearchResponse>('/search', { query });
    return response.data;
  },
};

export const workApi = {
  getLogs: async () => {
    const response = await apiClient.get<string[]>('/work/logs');
    return response.data;
  },
  getLog: async (date: string) => {
    const response = await apiClient.get<{ date: string, content: string }>(`/work/logs/${date}`);
    return response.data;
  },
  getEvaluation: async (period: string) => {
    const response = await apiClient.get<{ period: string, evaluation: string }>(`/work/evaluation/summary?period=${period}`);
    return response.data;
  }
};
