import { createSlice, createAsyncThunk, PayloadAction } from '@reduxjs/toolkit';
import { User, LoginResponse, RegisterResponse } from '../../types';
import apiService from '../../services/api';

interface AuthState {
  user: User | null;
  isAuthenticated: boolean;
  loading: boolean;
  error: string | null;
}

const initialState: AuthState = {
  user: null,
  isAuthenticated: !!localStorage.getItem('access_token'),
  loading: false,
  error: null,
};

/**
 * Parse Django REST Framework error responses into user-friendly messages.
 * Django errors can be: string, array of strings, or object with field keys.
 */
function parseApiError(error: any): string {
  if (!error) return 'Something went wrong. Please try again.';

  // Axios error with response data
  const data = error?.response?.data;
  if (!data) {
    if (error?.message) return error.message;
    return 'Network error. Please check your connection.';
  }

  // Single string error
  if (typeof data === 'string') return data;

  // { detail: "..." } format (DRF default)
  if (data.detail) return data.detail;

  // { non_field_errors: ["..."] }
  if (data.non_field_errors) {
    return Array.isArray(data.non_field_errors)
      ? data.non_field_errors.join(' ')
      : data.non_field_errors;
  }

  // { field: ["error1", "error2"], ... } format
  if (typeof data === 'object') {
    const messages: string[] = [];
    for (const [field, errors] of Object.entries(data)) {
      const fieldName = field
        .replace(/_/g, ' ')
        .replace(/\b\w/g, (c) => c.toUpperCase());
      if (Array.isArray(errors)) {
        messages.push(`${fieldName}: ${(errors as string[]).join(' ')}`);
      } else if (typeof errors === 'string') {
        messages.push(`${fieldName}: ${errors}`);
      }
    }
    if (messages.length > 0) return messages.join('\n');
  }

  return 'Something went wrong. Please try again.';
}

export const login = createAsyncThunk(
  'auth/login',
  async ({ email, password }: { email: string; password: string }, { rejectWithValue }) => {
    try {
      const response = await apiService.login(email, password);
      return response;
    } catch (error: any) {
      return rejectWithValue(parseApiError(error));
    }
  }
);

export const register = createAsyncThunk(
  'auth/register',
  async (userData: {
    username: string;
    email: string;
    password: string;
    password_confirm: string;
    full_name?: string;
    country?: string;
    age?: number;
  }, { rejectWithValue }) => {
    try {
      const response = await apiService.register(userData);
      return response;
    } catch (error: any) {
      return rejectWithValue(parseApiError(error));
    }
  }
);

export const logout = createAsyncThunk('auth/logout', async () => {
  await apiService.logout();
});

export const getCurrentUser = createAsyncThunk('auth/getCurrentUser', async () => {
  const response = await apiService.getCurrentUser();
  return response;
});

const authSlice = createSlice({
  name: 'auth',
  initialState,
  reducers: {
    clearError: (state) => {
      state.error = null;
    },
  },
  extraReducers: (builder) => {
    builder
      // Login
      .addCase(login.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(login.fulfilled, (state, action: PayloadAction<LoginResponse>) => {
        state.loading = false;
        state.user = action.payload.user;
        state.isAuthenticated = true;
      })
      .addCase(login.rejected, (state, action) => {
        state.loading = false;
        state.error = (action.payload as string) || 'Invalid email or password. Please try again.';
      })
      // Register
      .addCase(register.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(register.fulfilled, (state, action: PayloadAction<RegisterResponse>) => {
        state.loading = false;
        state.user = action.payload.user;
        state.isAuthenticated = true;
      })
      .addCase(register.rejected, (state, action) => {
        state.loading = false;
        state.error = (action.payload as string) || 'Registration failed. Please try again.';
      })
      // Logout
      .addCase(logout.fulfilled, (state) => {
        state.user = null;
        state.isAuthenticated = false;
      })
      // Get current user
      .addCase(getCurrentUser.fulfilled, (state, action: PayloadAction<User>) => {
        state.user = action.payload;
        state.isAuthenticated = true;
      })
      .addCase(getCurrentUser.rejected, (state) => {
        state.user = null;
        state.isAuthenticated = false;
      });
  },
});

export const { clearError } = authSlice.actions;
export default authSlice.reducer;
