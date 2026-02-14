import { createSlice, createAsyncThunk, PayloadAction } from '@reduxjs/toolkit';
import { Profile } from '../../types';
import apiService from '../../services/api';

interface ProfileState {
  profile: Profile | null;
  loading: boolean;
  error: string | null;
}

const initialState: ProfileState = {
  profile: null,
  loading: false,
  error: null,
};

export const fetchProfile = createAsyncThunk('profile/fetchProfile', async () => {
  const response = await apiService.getProfile();
  return response;
});

export const updateProfile = createAsyncThunk(
  'profile/updateProfile',
  async (profileData: Partial<Profile>) => {
    const response = await apiService.updateProfile(profileData);
    return response;
  }
);

export const createProfile = createAsyncThunk(
  'profile/createProfile',
  async (profileData: Partial<Profile>) => {
    const response = await apiService.createProfile(profileData);
    return response;
  }
);

const profileSlice = createSlice({
  name: 'profile',
  initialState,
  reducers: {
    clearError: (state) => {
      state.error = null;
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(fetchProfile.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchProfile.fulfilled, (state, action: PayloadAction<Profile>) => {
        state.loading = false;
        state.profile = action.payload;
      })
      .addCase(fetchProfile.rejected, (state, action) => {
        state.loading = false;
        state.error = action.error.message || 'Failed to fetch profile';
      })
      .addCase(updateProfile.fulfilled, (state, action: PayloadAction<Profile>) => {
        state.profile = action.payload;
      })
      .addCase(createProfile.fulfilled, (state, action: PayloadAction<Profile>) => {
        state.profile = action.payload;
      });
  },
});

export const { clearError } = profileSlice.actions;
export default profileSlice.reducer;

