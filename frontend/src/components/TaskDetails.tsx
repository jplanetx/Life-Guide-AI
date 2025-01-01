import React, { useState } from 'react';
import { Task } from '../services/TaskService';
import { Save, X } from 'lucide-react';

interface TaskDetailsProps {
  task: Task | null;
  onClose: () => void;
  onSave: (task: Task) => Promise<void>;
}

const TaskDetails: React.FC<TaskDetailsProps> = ({ task, onClose, onSave }) => {
  const [editing, setEditing] = useState<Task | null>(task);

  if (!task || !editing) return null;

  const handleSave = async () => {
    if (editing) {
      await onSave(editing);
      setEditing(null);
    }
  };

  return (
    <div className="space-y-4">
      <div className="flex justify-between items-center">
        <input
          className="text-xl font-semibold bg-transparent border-b border-gray-300 focus:border-blue-500 outline-none w-full"
          value={editing.title}
          onChange={e => setEditing({ ...editing, title: e.target.value })}
        />
        <button onClick={onClose} className="p-1 hover:bg-gray-100 rounded">
          <X size={20} />
        </button>
      </div>

      <div className="space-y-4">
        <div>
          <label className="block text-sm font-medium text-gray-700">Status</label>
          <select
            className="mt-1 block w-full rounded border-gray-300 shadow-sm"
            value={editing.status}
            onChange={e => setEditing({ ...editing, status: e.target.value })}
          >
            <option>Not Started</option>
            <option>In Progress</option>
            <option>Completed</option>
          </select>
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700">Importance</label>
          <select
            className="mt-1 block w-full rounded border-gray-300 shadow-sm"
            value={editing.importance}
            onChange={e => setEditing({ ...editing, importance: e.target.value as Task['importance'] })}
          >
            <option>High</option>
            <option>Medium</option>
            <option>Low</option>
          </select>
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700">Urgency</label>
          <select
            className="mt-1 block w-full rounded border-gray-300 shadow-sm"
            value={editing.urgency}
            onChange={e => setEditing({ ...editing, urgency: e.target.value as Task['urgency'] })}
          >
            <option>High</option>
            <option>Medium</option>
            <option>Low</option>
          </select>
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700">Due Date</label>
          <input
            type="date"
            className="mt-1 block w-full rounded border-gray-300 shadow-sm"
            value={editing.dueDate || ''}
            onChange={e => setEditing({ ...editing, dueDate: e.target.value })}
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700">Description</label>
          <textarea
            className="mt-1 block w-full rounded border-gray-300 shadow-sm"
            rows={3}
            value={editing.description || ''}
            onChange={e => setEditing({ ...editing, description: e.target.value })}
          />
        </div>

        <button
          onClick={handleSave}
          className="w-full flex items-center justify-center space-x-2 bg-blue-500 text-white py-2 px-4 rounded hover:bg-blue-600"
        >
          <Save size={16} />
          <span>Save Changes</span>
        </button>
      </div>
    </div>
  );
};

export default TaskDetails;
