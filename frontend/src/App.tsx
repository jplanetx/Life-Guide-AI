import React, { useState, useEffect } from 'react';
import DashboardLayout from './components/DashboardLayout';
import { EisenhowerMatrix } from './components/EisenhowerMatrix';
import TaskDetails from './components/TaskDetails';
import { taskService, Task } from './services/TaskService';
import { Plus, Loader } from 'lucide-react';

const App: React.FC = () => {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [selectedTask, setSelectedTask] = useState<Task | null>(null);
  const [isDetailsOpen, setIsDetailsOpen] = useState(false);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    loadTasks();
  }, []);

  const loadTasks = async () => {
    try {
      console.log('Starting to load tasks...'); // Debug log
      setIsLoading(true);
      setError(null);
      const loadedTasks = await taskService.getAllTasks();
      console.log('Loaded tasks:', loadedTasks); // Debug log
      setTasks(loadedTasks);
      console.log('Tasks set in state:', loadedTasks.length); // Debug log
    } catch (err) {
      console.error('Error loading tasks:', err);
      setError('Failed to load tasks. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleTaskClick = (task: Task) => {
    setSelectedTask(task);
    setIsDetailsOpen(true);
  };

  const handleTaskSave = async (updatedTask: Task) => {
    try {
      await taskService.updateTask(updatedTask.id, updatedTask);
      await loadTasks();
      setIsDetailsOpen(false);
    } catch (err) {
      console.error('Error updating task:', err);
    }
  };

  const handleAddTask = async () => {
    try {
      const newTask = {
        title: 'New Task',
        importance: 'Medium' as const,
        urgency: 'Medium' as const,
        status: 'Not Started',
      };

      const createdTask = await taskService.addTask(newTask);
      console.log('Created new task:', createdTask); // Debug log
      setTasks([...tasks, createdTask]);
      setSelectedTask(createdTask);
      setIsDetailsOpen(true);
    } catch (err) {
      console.error('Error creating task:', err);
    }
  };

  // Debug log to check current state
  console.log('Current tasks in state:', tasks);

  return (
    <DashboardLayout>
      <div className="h-full flex flex-col">
        <div className="flex justify-between items-center mb-4">
          <h1 className="text-2xl font-bold">Task Management</h1>
          <button
            onClick={handleAddTask}
            className="flex items-center space-x-2 bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
          >
            <Plus size={20} />
            <span>Add Task</span>
          </button>
        </div>

        {isLoading ? (
          <div className="flex items-center justify-center h-full">
            <Loader className="animate-spin" size={32} />
          </div>
        ) : (
          <>
            <div className="mb-4">
              <p className="text-sm text-gray-600">
                Total tasks: {tasks.length}
              </p>
            </div>
            <EisenhowerMatrix
              tasks={tasks}
              onTaskClick={handleTaskClick}
            />
          </>
        )}

        {isDetailsOpen && (
          <div className="fixed right-0 top-0 h-full w-80 bg-white shadow-lg">
            <TaskDetails
              task={selectedTask}
              onClose={() => setIsDetailsOpen(false)}
              onSave={handleTaskSave}
            />
          </div>
        )}
      </div>
    </DashboardLayout>
  );
};

export default App;
