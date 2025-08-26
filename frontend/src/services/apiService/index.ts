import axios, { AxiosInstance, AxiosRequestConfig } from 'axios';
import { AppConfig } from '@/configs/app.config';

export interface ApiActions {
  [key: string]: (api: RawService) => Record<string, (...args: any[]) => Promise<any>>;
}

export interface RawService {
  get: <T>(url: string, config?: AxiosRequestConfig) => Promise<T>;
  post: <T>(url: string, data?: any, config?: AxiosRequestConfig) => Promise<T>;
  put: <T>(url: string, data?: any, config?: AxiosRequestConfig) => Promise<T>;
  delete: <T>(url: string, config?: AxiosRequestConfig) => Promise<T>;
}

class ApiService {
  private client: AxiosInstance;

  constructor(baseURL: string, isSSR = false) {
    this.client = axios.create({
      baseURL,
      timeout: AppConfig.api.timeout,
    });

    if (!isSSR) {
      this.setupInterceptors();
    }
  }

  private setupInterceptors(): void {
    this.client.interceptors.request.use(
      (config) => {
        const token = localStorage.getItem(AppConfig.auth.tokenKey);
        if (token) {
          config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
      },
      (error) => Promise.reject(error)
    );

    this.client.interceptors.response.use(
      (response) => response.data,
      (error) => {
        if (error.response?.status === 401) {
          localStorage.removeItem(AppConfig.auth.tokenKey);
          window.location.href = '/login';
        }
        return Promise.reject(error);
      }
    );
  }

  get rawService(): RawService {
    return {
      get: <T>(url: string, config?: AxiosRequestConfig) => this.client.get<T>(url, config),
      post: <T>(url: string, data?: any, config?: AxiosRequestConfig) => this.client.post<T>(url, data, config),
      put: <T>(url: string, data?: any, config?: AxiosRequestConfig) => this.client.put<T>(url, data, config),
      delete: <T>(url: string, config?: AxiosRequestConfig) => this.client.delete<T>(url, config),
    };
  }
}

export const Api = new ApiService(AppConfig.api.baseUrl, true);
export const ClientApi = new ApiService(AppConfig.api.baseUrl, false);