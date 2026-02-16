import { createSlice, createAsyncThunk, PayloadAction } from '@reduxjs/toolkit';
import { Profile } from '../../types';
import apiService from '../../services/api';

interface ProfileState {
  profile: Profile | null;
  loading: boolean;
  error: string | null;
  updating: boolean;
  updateSuccess: boolean;
  updateError: string | null;
}

const initialState: ProfileState = {
  profile: null,
  loading: false,
  error: null,
  updating: false,
  updateSuccess: false,
  updateError: null,
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

export const uploadProfilePicture = createAsyncThunk(
  'profile/uploadProfilePicture',
  async (file: File) => {
    const response = await apiService.uploadProfilePicture(file);
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
    clearUpdateStatus: (state) => {
      state.updateSuccess = false;
      state.updateError = null;
    },
  },
  extraReducers: (builder) => {
    builder
      // Fetch
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
      // Update
      .addCase(updateProfile.pending, (state) => {
        state.updating = true;
        state.updateSuccess = false;
        state.updateError = null;
      })
      .addCase(updateProfile.fulfilled, (state, action: PayloadAction<Profile>) => {
        state.updating = false;
        state.updateSuccess = true;
        state.profile = action.payload;
      })
      .addCase(updateProfile.rejected, (state, action) => {
        state.updating = false;
        state.updateError = action.error.message || 'Failed to update profile';
      })
      // Upload Picture
      .addCase(uploadProfilePicture.pending, (state) => {
        state.updating = true;
        state.updateSuccess = false;
        state.updateError = null;
      })
      .addCase(uploadProfilePicture.fulfilled, (state, action: PayloadAction<Profile>) => {
        state.updating = false;
        state.updateSuccess = true;
        state.profile = action.payload;
      })
      .addCase(uploadProfilePicture.rejected, (state, action) => {
        state.updating = false;
        state.updateError = action.error.message || 'Failed to upload profile picture';
      })
      // Create
      .addCase(createProfile.fulfilled, (state, action: PayloadAction<Profile>) => {
        state.profile = action.payload;
      });
  },
});

export const { clearError, clearUpdateStatus } = profileSlice.actions;
export default profileSlice.reducer;
