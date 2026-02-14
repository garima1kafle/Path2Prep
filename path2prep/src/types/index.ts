// User types
export interface User {
  id: number;
  username: string;
  email: string;
  full_name: string;
  country: string;
  age?: number;
  role: 'student' | 'admin';
  is_email_verified: boolean;
}

// Profile types
export interface Profile {
  id: number;
  user: number;
  gpa?: number;
  degree_level: string;
  major: string;
  country: string;
  target_country: string;
  ielts_score?: number;
  toefl_score?: number;
  gre_score?: number;
  gmat_score?: number;
  income_range: string;
  need_based_preference: boolean;
  technical_skills: string[];
  soft_skills: string[];
  interests: string[];
  holland_code: string;
}

// Career types
export interface Career {
  id: number;
  name: string;
  description: string;
  category: string;
  required_skills: string[];
  average_salary?: number;
  growth_rate: string;
}

export interface CareerRecommendation {
  id: number;
  career: Career;
  confidence_score: number;
  model_used: string;
  rank: number;
}

// Scholarship types
export interface Scholarship {
  id: number;
  title: string;
  organization: string;
  description: string;
  eligibility: string;
  deadline?: string;
  country: string;
  funding_amount: string;
  link: string;
  is_approved: boolean;
  is_active: boolean;
}

export interface ScholarshipMatch {
  scholarship: Scholarship;
  relevance_score: number;
  method: string;
}

// Application types
export interface Application {
  id: number;
  user: number;
  scholarship: Scholarship;
  status: 'not_started' | 'in_progress' | 'submitted' | 'accepted' | 'rejected';
  notes: string;
  created_at: string;
  updated_at: string;
}

// Bookmark types
export interface Bookmark {
  id: number;
  user: number;
  scholarship: Scholarship;
  created_at: string;
}

// Notification types
export interface Notification {
  id: number;
  user: number;
  notification_type: 'new_match' | 'deadline_approaching' | 'profile_incomplete' | 'application_reminder';
  title: string;
  message: string;
  is_read: boolean;
  link?: string;
  scholarship_id?: number;
  application_id?: number;
  created_at: string;
}

// API Response types
export interface ApiResponse<T> {
  data?: T;
  error?: string;
  message?: string;
}

export interface LoginResponse {
  user: User;
  access: string;
  refresh: string;
}

export interface RegisterResponse {
  user: User;
  access: string;
  refresh: string;
}

