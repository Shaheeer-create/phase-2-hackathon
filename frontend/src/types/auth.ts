export interface User {
  id: number;
  email: string;
  username?: string;
  email_verified: boolean;
  created_at: Date;
  updated_at: Date;
}

export interface Task {
  id: number;
  title: string;
  description?: string;
  completed: boolean;
  due_date?: string; // Format: YYYY-MM-DD
  due_time?: string; // Format: HH:MM
  priority: 'high' | 'medium' | 'low';
  tags?: string;
  user_id: number;
  version: number;
  created_at: Date;
  updated_at: Date;
}