import { createSlice, createAsyncThunk, PayloadAction } from '@reduxjs/toolkit';
import { Notification } from '../../types';
import apiService from '../../services/api';

interface NotificationState {
  notifications: Notification[];
  unreadCount: number;
  loading: boolean;
  error: string | null;
}

const initialState: NotificationState = {
  notifications: [],
  unreadCount: 0,
  loading: false,
  error: null,
};

export const fetchNotifications = createAsyncThunk('notifications/fetchNotifications', async () => {
  const response = await apiService.getNotifications();
  return response;
});

export const fetchUnreadCount = createAsyncThunk('notifications/fetchUnreadCount', async () => {
  const response = await apiService.getUnreadCount();
  return response.unread_count;
});

export const markNotificationRead = createAsyncThunk(
  'notifications/markNotificationRead',
  async (id: number) => {
    await apiService.markNotificationRead(id);
    return id;
  }
);

export const markAllNotificationsRead = createAsyncThunk(
  'notifications/markAllNotificationsRead',
  async () => {
    await apiService.markAllNotificationsRead();
  }
);

const notificationSlice = createSlice({
  name: 'notifications',
  initialState,
  reducers: {
    clearError: (state) => {
      state.error = null;
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(fetchNotifications.fulfilled, (state, action: PayloadAction<Notification[]>) => {
        state.notifications = action.payload;
      })
      .addCase(fetchUnreadCount.fulfilled, (state, action: PayloadAction<number>) => {
        state.unreadCount = action.payload;
      })
      .addCase(markNotificationRead.fulfilled, (state, action: PayloadAction<number>) => {
        const notification = state.notifications.find((n) => n.id === action.payload);
        if (notification) {
          notification.is_read = true;
        }
        state.unreadCount = Math.max(0, state.unreadCount - 1);
      })
      .addCase(markAllNotificationsRead.fulfilled, (state) => {
        state.notifications.forEach((n) => {
          n.is_read = true;
        });
        state.unreadCount = 0;
      });
  },
});

export const { clearError } = notificationSlice.actions;
export default notificationSlice.reducer;

