import { createSlice, createAsyncThunk, PayloadAction } from '@reduxjs/toolkit';
import { Scholarship, ScholarshipMatch, Application, Bookmark } from '../../types';
import apiService from '../../services/api';

interface ScholarshipState {
  scholarships: Scholarship[];
  matches: ScholarshipMatch[];
  applications: Application[];
  bookmarks: Bookmark[];
  loading: boolean;
  matchLoading: boolean;
  error: string | null;
}

const initialState: ScholarshipState = {
  scholarships: [],
  matches: [],
  applications: [],
  bookmarks: [],
  loading: false,
  matchLoading: false,
  error: null,
};

export const fetchScholarships = createAsyncThunk(
  'scholarships/fetchScholarships',
  async (params?: { country?: string; search?: string }) => {
    const response = await apiService.getScholarships(params);
    return response.results;
  }
);

export const matchScholarships = createAsyncThunk(
  'scholarships/matchScholarships',
  async (top_k?: number) => {
    const response = await apiService.matchScholarships(top_k);
    return response.matches;
  }
);

export const fetchApplications = createAsyncThunk('scholarships/fetchApplications', async () => {
  const response = await apiService.getApplications();
  return response;
});

export const fetchBookmarks = createAsyncThunk('scholarships/fetchBookmarks', async () => {
  const response = await apiService.getBookmarks();
  return response;
});

const scholarshipSlice = createSlice({
  name: 'scholarships',
  initialState,
  reducers: {
    clearError: (state) => {
      state.error = null;
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(fetchScholarships.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchScholarships.fulfilled, (state, action: PayloadAction<Scholarship[]>) => {
        state.loading = false;
        state.scholarships = action.payload;
      })
      .addCase(fetchScholarships.rejected, (state, action) => {
        state.loading = false;
        state.error = action.error.message || 'Failed to fetch scholarships';
      })
      .addCase(matchScholarships.pending, (state) => {
        state.matchLoading = true;
        state.error = null;
      })
      .addCase(matchScholarships.fulfilled, (state, action: PayloadAction<ScholarshipMatch[]>) => {
        state.matchLoading = false;
        state.matches = action.payload;
      })
      .addCase(matchScholarships.rejected, (state, action) => {
        state.matchLoading = false;
        state.error = action.error.message || 'Failed to match scholarships';
      })
      .addCase(fetchApplications.fulfilled, (state, action: PayloadAction<Application[]>) => {
        state.applications = action.payload;
      })
      .addCase(fetchBookmarks.fulfilled, (state, action: PayloadAction<Bookmark[]>) => {
        state.bookmarks = action.payload;
      });
  },
});

export const { clearError } = scholarshipSlice.actions;
export default scholarshipSlice.reducer;

