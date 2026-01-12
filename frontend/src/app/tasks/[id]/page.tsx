'use client';

import { useState, useEffect } from 'react';
import { useRouter, useParams } from 'next/navigation';

const TaskDetailPage = () => {
  const { id } = useParams();
  const [task, setTask] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const router = useRouter();

  useEffect(() => {
    const fetchTask = async () => {
      try {
        // Check if user is authenticated
        const token = localStorage.getItem('access_token');
        if (!token) {
          router.push('/login');
          return;
        }

        // In a real implementation, this would fetch from the API
        // const response = await apiClient.getTask(userId, parseInt(id as string));
        // setTask(response.data.task);
        
        // For now, using mock data
        setTask({
          id: parseInt(id as string),
          title: 'Sample Task',
          description: 'This is a sample task description',
          completed: false,
          due_date: '2026-01-15',
          due_time: '18:00',
          priority: 'medium',
          tags: ['sample', 'mock'],
          user_id: 1,
          created_at: new Date().toISOString(),
          updated_at: new Date().toISOString(),
          version: 1
        });
      } catch (err: any) {
        console.error('Error fetching task:', err);
        setError(err.message || 'Failed to fetch task');
      } finally {
        setLoading(false);
      }
    };

    fetchTask();
  }, [id, router]);

  if (loading) {
    return <div>Loading task...</div>;
  }

  if (!task) {
    return <div>Task not found</div>;
  }

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-2xl font-bold mb-4">{task.title}</h1>
      
      {error && (
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
          {error}
        </div>
      )}
      
      <div className="bg-white shadow rounded-lg p-6">
        <div className="mb-4">
          <h2 className="text-lg font-semibold text-gray-700">Description</h2>
          <p className="text-gray-600">{task.description || 'No description provided'}</p>
        </div>
        
        <div className="grid grid-cols-2 gap-4 mb-4">
          <div>
            <h2 className="text-lg font-semibold text-gray-700">Due Date</h2>
            <p className="text-gray-600">{task.due_date || 'No due date'}</p>
          </div>
          <div>
            <h2 className="text-lg font-semibold text-gray-700">Due Time</h2>
            <p className="text-gray-600">{task.due_time || 'No due time'}</p>
          </div>
        </div>
        
        <div className="grid grid-cols-2 gap-4 mb-4">
          <div>
            <h2 className="text-lg font-semibold text-gray-700">Priority</h2>
            <p className="text-gray-600 capitalize">{task.priority}</p>
          </div>
          <div>
            <h2 className="text-lg font-semibold text-gray-700">Status</h2>
            <p className={`text-gray-600 ${task.completed ? 'text-green-600' : 'text-yellow-600'}`}>
              {task.completed ? 'Completed' : 'Pending'}
            </p>
          </div>
        </div>
        
        <div className="mb-6">
          <h2 className="text-lg font-semibold text-gray-700">Tags</h2>
          <div className="flex flex-wrap gap-2 mt-2">
            {(task.tags || []).map((tag: string, index: number) => (
              <span 
                key={index} 
                className="bg-blue-100 text-blue-800 text-xs px-2 py-1 rounded"
              >
                {tag}
              </span>
            ))}
          </div>
        </div>
        
        <div className="flex space-x-4">
          <button className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">
            Edit Task
          </button>
          <button 
            className={`${
              task.completed 
                ? 'bg-yellow-500 hover:bg-yellow-700' 
                : 'bg-green-500 hover:bg-green-700'
            } text-white font-bold py-2 px-4 rounded`}
          >
            {task.completed ? 'Mark Pending' : 'Mark Complete'}
          </button>
          <button className="bg-red-500 hover:bg-red-700 text-white font-bold py-2 px-4 rounded">
            Delete Task
          </button>
        </div>
      </div>
    </div>
  );
};

export default TaskDetailPage;