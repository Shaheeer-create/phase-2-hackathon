import { Task } from '../../types/auth';

interface TaskListProps {
  tasks: Task[];
  onTaskToggle?: (task: Task) => void;
  onTaskDelete?: (taskId: number) => void;
}

const TaskList = ({ tasks, onTaskToggle, onTaskDelete }: TaskListProps) => {
  return (
    <div className="grid grid-cols-1 gap-4">
      {tasks.map((task) => (
        <div 
          key={task.id} 
          className={`border rounded-lg p-4 ${task.completed ? 'bg-green-50' : 'bg-white'}`}
        >
          <div className="flex justify-between items-start">
            <div>
              <h3 className={`text-lg ${task.completed ? 'line-through text-gray-500' : 'text-gray-800'}`}>
                {task.title}
              </h3>
              {task.description && (
                <p className="text-gray-600 mt-1">{task.description}</p>
              )}
              {task.due_date && (
                <p className="text-sm text-gray-600">Due: {task.due_date}</p>
              )}
              <p className="text-sm text-gray-600">Priority: {task.priority}</p>
            </div>
            <div className="flex space-x-2">
              <button 
                onClick={() => onTaskToggle && onTaskToggle(task)}
                className={`${
                  task.completed ? 'text-yellow-500 hover:text-yellow-700' : 'text-green-500 hover:text-green-700'
                }`}
              >
                {task.completed ? 'Mark Pending' : 'Mark Complete'}
              </button>
              <button 
                onClick={() => onTaskDelete && onTaskDelete(task.id)}
                className="text-red-500 hover:text-red-700"
              >
                Delete
              </button>
            </div>
          </div>
        </div>
      ))}
    </div>
  );
};

export default TaskList;