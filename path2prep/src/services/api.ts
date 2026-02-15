import axios, { AxiosInstance, AxiosError } from 'axios';
import {
  User,
  Profile,
  CareerRecommendation,
  ScholarshipMatch,
  Application,
  Bookmark,
  Notification,
  LoginResponse,
  RegisterResponse,
} from '../types';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

class ApiService {
  private api: AxiosInstance;

  constructor() {
    this.api = axios.create({
      baseURL: API_BASE_URL,
      headers: {
        'Content-Type': 'application/json',
      },
    });

    // Add request interceptor to include auth token
    this.api.interceptors.request.use(
      (config) => {
        const token = localStorage.getItem('access_token');
        if (token) {
          config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
      },
      (error) => {
        return Promise.reject(error);
      }
    );

    // Add response interceptor to handle token refresh
    this.api.interceptors.response.use(
      (response) => response,
      async (error: AxiosError) => {
        const originalRequest = error.config as any;

        if (error.response?.status === 401 && !originalRequest._retry) {
          originalRequest._retry = true;

          try {
            const refreshToken = localStorage.getItem('refresh_token');
            if (refreshToken) {
              const response = await axios.post(`${API_BASE_URL}/auth/token/refresh/`, {
                refresh: refreshToken,
              });
              const { access } = response.data;
              localStorage.setItem('access_token', access);
              originalRequest.headers.Authorization = `Bearer ${access}`;
              return this.api(originalRequest);
            }
          } catch (refreshError) {
            localStorage.removeItem('access_token');
            localStorage.removeItem('refresh_token');
            window.location.href = '/login';
            return Promise.reject(refreshError);
          }
        }

        return Promise.reject(error);
      }
    );
  }

  // Authentication
  async login(email: string, password: string): Promise<LoginResponse> {
    const response = await this.api.post('/auth/login/', { email, password });
    const data = response.data;
    localStorage.setItem('access_token', data.access);
    localStorage.setItem('refresh_token', data.refresh);
    return data;
  }

  async register(userData: {
    username: string;
    email: string;
    password: string;
    password_confirm: string;
    full_name?: string;
    country?: string;
    age?: number;
  }): Promise<RegisterResponse> {
    const response = await this.api.post('/auth/users/register/', userData);
    const data = response.data;
    localStorage.setItem('access_token', data.access);
    localStorage.setItem('refresh_token', data.refresh);
    return data;
  }

  async logout(): Promise<void> {
    const refreshToken = localStorage.getItem('refresh_token');
    if (refreshToken) {
      await this.api.post('/auth/users/logout/', { refresh_token: refreshToken });
    }
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
  }

  async getCurrentUser(): Promise<User> {
    const response = await this.api.get('/auth/users/me/');
    return response.data;
  }

  // Profile
  async getProfile(): Promise<Profile> {
    const response = await this.api.get('/profiles/me/');
    return response.data;
  }

  async updateProfile(profileData: Partial<Profile>): Promise<Profile> {
    const response = await this.api.patch('/profiles/me/', profileData);
    return response.data;
  }

  async createProfile(profileData: Partial<Profile>): Promise<Profile> {
    const response = await this.api.post('/profiles/profiles/', profileData);
    return response.data;
  }

  // Career Recommendations
  async getCareerRecommendations(): Promise<{ top_careers: Array<{ career: string; confidence: number; description: string; category: string }> }> {
    const response = await this.api.post('/recommend-career/recommend/');
    return response.data;
  }

  async getMyRecommendations(): Promise<CareerRecommendation[]> {
    const response = await this.api.get('/recommend-career/my_recommendations/');
    return response.data;
  }

  // Scholarships
  async getScholarships(params?: {
    country?: string;
    search?: string;
    ordering?: string;
  }): Promise<{ results: any[]; count: number }> {
    const response = await this.api.get('/scholarships/', { params });
    return response.data;
  }

  async getScholarship(id: number): Promise<any> {
    const response = await this.api.get(`/scholarships/${id}/`);
    return response.data;
  }

  async matchScholarships(top_k?: number): Promise<{ matches: ScholarshipMatch[] }> {
    const response = await this.api.post('/scholarships/match/', { top_k: top_k || 5 });
    return response.data;
  }

  // Applications
  async getApplications(): Promise<Application[]> {
    const response = await this.api.get('/applications/');
    return response.data;
  }

  async createApplication(scholarshipId: number, status?: string): Promise<Application> {
    const response = await this.api.post('/applications/', {
      scholarship_id: scholarshipId,
      status: status || 'not_started',
    });
    return response.data;
  }

  async updateApplication(id: number, data: Partial<Application>): Promise<Application> {
    const response = await this.api.patch(`/applications/${id}/`, data);
    return response.data;
  }

  // Bookmarks
  async getBookmarks(): Promise<Bookmark[]> {
    const response = await this.api.get('/bookmarks/');
    return response.data;
  }

  async createBookmark(scholarshipId: number): Promise<Bookmark> {
    const response = await this.api.post('/bookmarks/', {
      scholarship_id: scholarshipId,
    });
    return response.data;
  }

  async deleteBookmark(id: number): Promise<void> {
    await this.api.delete(`/bookmarks/${id}/`);
  }

  // Notifications
  async getNotifications(): Promise<Notification[]> {
    const response = await this.api.get('/notifications/');
    return response.data;
  }

  async markNotificationRead(id: number): Promise<void> {
    await this.api.post(`/notifications/${id}/mark_read/`);
  }

  async markAllNotificationsRead(): Promise<void> {
    await this.api.post('/notifications/mark_all_read/');
  }

  async getUnreadCount(): Promise<{ unread_count: number }> {
    const response = await this.api.get('/notifications/unread_count/');
    return response.data;
  }
}

export const apiService = new ApiService();
export default apiService;

