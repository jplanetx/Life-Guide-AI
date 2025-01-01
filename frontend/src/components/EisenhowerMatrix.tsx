import React from 'react';
import { Task } from '../services/TaskService';

interface QuadrantProps {
  title: string;
  tasks: Task[];
  description: string;
  bgColor: string;
  onTaskClick: (task: Task) => void;
}

const Quadrant: React.FC<QuadrantProps> = ({
  title,
  tasks,
  description,
  bgColor,
  onTaskClick
}) => (
  <div className={`p-4 rounded-lg shadow-lg ${bgColor} h-full flex flex-col`}>
    <h3 className="font-bold text-lg mb-2">{title}</h3>
    <p className="text-sm text-gray-600 mb-4">{description}</p>
    <div className="space-y-2 flex-grow overflow-auto">
      {tasks.map(task => (
        <div
          key={task.id}
          onClick={() => onTaskClick(task)}
          className="p-3 bg-white rounded-lg shadow hover:shadow-md transition-shadow cursor-pointer"
        >
          <p className="font-medium">{task.title}</p>
          <div className="flex gap-2 mt-2">
            <span className={`text-xs px-2 py-1 rounded ${
              task.importance === 'High' ? 'bg-red-100 text-red-800' :
              task.importance === 'Medium' ? 'bg-yellow-100 text-yellow-800' :
              'bg-green-100 text-green-800'
            }`}>
              {task.importance}
            </span>
            <span className={`text-xs px-2 py-1 rounded ${
              task.urgency === 'High' ? 'bg-purple-100 text-purple-800' :
              task.urgency === 'Medium' ? 'bg-blue-100 text-blue-800' :
              'bg-gray-100 text-gray-800'
            }`}>
              {task.urgency}
            </span>
            <span className="text-xs px-2 py-1 rounded bg-gray-100 text-gray-800">
              {task.status}
            </span>
          </div>
          {task.dueDate && (
            <div className="text-xs text-gray-500 mt-2">
              Due: {new Date(task.dueDate).toLocaleDateString()}
            </div>
          )}
        </div>
      ))}
      {tasks.length === 0 && (
        <div className="text-center text-gray-500 italic">
          No tasks in this quadrant
        </div>
      )}
    </div>
  </div>
);

interface EisenhowerMatrixProps {
  tasks: Task[];
  onTaskClick: (task: Task) => void;
}

export const EisenhowerMatrix: React.FC<EisenhowerMatrixProps> = ({
  tasks = [],
  onTaskClick
}) => {
  console.log('Tasks in matrix:', tasks); // Debug log

  // Helper function to normalize property values
  const normalizeValue = (value: string | undefined): string =>
    (value || '').toLowerCase().trim();

  const categorizedTasks = {
    important_urgent: tasks.filter(t =>
      normalizeValue(t.importance) === 'high' &&
      normalizeValue(t.urgency) === 'high'
    ),
    important_not_urgent: tasks.filter(t =>
      normalizeValue(t.importance) === 'high' &&
      normalizeValue(t.urgency) !== 'high'
    ),
    not_important_urgent: tasks.filter(t =>
      normalizeValue(t.importance) !== 'high' &&
      normalizeValue(t.urgency) === 'high'
    ),
    not_important_not_urgent: tasks.filter(t =>
      normalizeValue(t.importance) !== 'high' &&
      normalizeValue(t.urgency) !== 'high'
    )
  };

  // Debug logs
  console.log('Categorized tasks:', {
    important_urgent: categorizedTasks.important_urgent.length,
    important_not_urgent: categorizedTasks.important_not_urgent.length,
    not_important_urgent: categorizedTasks.not_important_urgent.length,
    not_important_not_urgent: categorizedTasks.not_important_not_urgent.length
  });

  return (
    <div className="grid grid-cols-2 gap-4 p-4 h-[calc(100vh-200px)]">
      <Quadrant
        title="Do First"
        tasks={categorizedTasks.important_urgent}
        description="Important and urgent tasks that need immediate attention"
        bgColor="bg-red-50"
        onTaskClick={onTaskClick}
      />
      <Quadrant
        title="Schedule"
        tasks={categorizedTasks.important_not_urgent}
        description="Important but not urgent tasks to plan for later"
        bgColor="bg-blue-50"
        onTaskClick={onTaskClick}
      />
      <Quadrant
        title="Delegate or Do Fast"
        tasks={categorizedTasks.not_important_urgent}
        description="Urgent but less important tasks to minimize"
        bgColor="bg-yellow-50"
        onTaskClick={onTaskClick}
      />
      <Quadrant
        title="Eliminate or Postpone"
        tasks={categorizedTasks.not_important_not_urgent}
        description="Neither urgent nor important tasks to reconsider"
        bgColor="bg-green-50"
        onTaskClick={onTaskClick}
      />
    </div>
  );
};

export default EisenhowerMatrix;
