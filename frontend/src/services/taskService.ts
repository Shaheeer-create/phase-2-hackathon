import api from '../lib/api';

export interface Task {
  id: number;
  title: string;
  description?: string;
  completed: boolean;
  due_date?: string;
  priority: 'low' | 'medium' | 'high';
  user_id: number;
  created_at: string;
  updated_at: string;
}

export interface CreateTaskData {
  title: string;
  description?: string;
  due_date?: string;
  priority: 'low' | 'medium' | 'high';
}

export interface UpdateTaskData {
  title?: string;
  description?: string;
  completed?: boolean;
  due_date?: string;
  priority?: 'low' | 'medium' | 'high';
}

// Helper function to get user ID from token
const getUserIdFromToken = (): number | null => {
  const token = localStorage.getItem('access_token');
  if (!token) {
    console.error('No access token found in localStorage');
    return null;
  }

  try {
    // Decode JWT token to get user ID
    const base64Url = token.split('.')[1];
    const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
    // Add padding if needed
    const padding = '='.repeat((4 - (base64.length % 4)) % 4);
    const base64Padded = base64 + padding;
    const jsonPayload = atob(base64Padded);
    const decodedToken = JSON.parse(jsonPayload);

    if (!decodedToken.user_id) {
      console.error('No user_id found in token payload:', decodedToken);
      return null;
    }

    console.log('Successfully extracted user_id from token:', decodedToken.user_id);
    return decodedToken.user_id;
  } catch (error) {
    console.error('Error decoding token:', error);
    console.error('Problematic token (first 50 chars):', token.substring(0, 50));
    return null;
  }
};

export const taskService = {
  // Get all tasks for the authenticated user
  getTasks: async (): Promise<Task[]> => {
    try {
      const userId = getUserIdFromToken();
      if (!userId) {
        throw new Error('User not authenticated');
      }
      
      const response = await api.get(`/${userId}/tasks`);
      return response.data;
    } catch (error) {
      console.error('Error fetching tasks:', error);
      throw error;
    }
  },

  // Create a new task
  createTask: async (taskData: CreateTaskData): Promise<Task> => {
    try {
      const userId = getUserIdFromToken();
      if (!userId) {
        throw new Error('User not authenticated');
      }

      console.log('Creating task with userId:', userId);
      console.log('Task data:', taskData);
      console.log('Access token exists:', !!localStorage.getItem('access_token'));

      const response = await api.post(`/${userId}/tasks`, taskData);
      console.log('Task creation response:', response);
      return response.data;
    } catch (error: any) {
      console.error('Error creating task:', error);
      console.error('Error details:', {
        message: error.message,
        code: error.code,
        response: error.response?.data,
        status: error.response?.status,
        statusText: error.response?.statusText,
        requestUrl: error.config?.url,
        requestMethod: error.config?.method,
        requestHeaders: error.config?.headers
      });
      throw error;
    }
  },

  // Update an existing task
  updateTask: async (taskId: number, taskData: UpdateTaskData): Promise<Task> => {
    try {
      const userId = getUserIdFromToken();
      if (!userId) {
        throw new Error('User not authenticated');
      }
      
      const response = await api.put(`/${userId}/tasks/${taskId}`, taskData);
      return response.data;
    } catch (error) {
      console.error('Error updating task:', error);
      throw error;
    }
  },

  // Delete a task
  deleteTask: async (taskId: number): Promise<void> => {
    try {
      const userId = getUserIdFromToken();
      if (!userId) {
        throw new Error('User not authenticated');
      }
      
      await api.delete(`/${userId}/tasks/${taskId}`);
    } catch (error) {
      console.error('Error deleting task:', error);
      throw error;
    }
  },

  // Toggle task completion status
  toggleTaskCompletion: async (taskId: number): Promise<Task> => {
    try {
      const userId = getUserIdFromToken();
      if (!userId) {
        throw new Error('User not authenticated');
      }
      
      const response = await api.patch(`/${userId}/tasks/${taskId}/complete`);
      return response.data;
    } catch (error) {
      console.error('Error toggling task completion:', error);
      throw error;
    }
  },
};