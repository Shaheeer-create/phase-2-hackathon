import Link from 'next/link';
import { Task } from '../../types/auth';

interface TaskCardProps {
  task: Task;
  onToggleCompletion?: (task: Task) => void;
  onDelete?: (taskId: number) => void;
}

const TaskCard = ({ task, onToggleCompletion, onDelete }: TaskCardProps) => {
  return (
    <div className={`border rounded-lg p-4 ${task.completed ? 'bg-green-50' : 'bg-white'}`}>
      <div className="flex justify-between items-start">
        <div>
          <h3 className={`text-lg font-medium ${task.completed ? 'line-through text-gray-500' : 'text-gray-800'}`}>
            {task.title}
          </h3>
          {task.description && (
            <p className="text-gray-600 mt-1">{task.description}</p>
          )}
          {task.due_date && (
            <p className="text-sm text-gray-600 mt-1">Due: {task.due_date}</p>
          )}
          <p className="text-sm text-gray-600 mt-1">Priority: {task.priority}</p>
        </div>
        <div className="flex space-x-2">
          <button
            onClick={() => onToggleCompletion && onToggleCompletion(task)}
            className={`${
              task.completed
                ? 'text-yellow-500 hover:text-yellow-700'
                : 'text-green-500 hover:text-green-700'
            }`}
          >
            {task.completed ? 'Mark Pending' : 'Mark Complete'}
          </button>
          <button 
            onClick={() => onDelete && onDelete(task.id)}
            className="text-red-500 hover:text-red-700"
          >
            Delete
          </button>
          <Link 
            href={`/tasks/${task.id}`} 
            className="text-blue-500 hover:text-blue-700"
          >
            Edit
          </Link>
        </div>
      </div>
    </div>
  );
};

export default TaskCard;