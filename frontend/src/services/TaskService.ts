export interface Task {
  id: string;
  title: string;
  importance: 'High' | 'Medium' | 'Low';
  urgency: 'High' | 'Medium' | 'Low';
  status: string;
  description?: string;  // Added this
  dueDate?: string;
  energy?: string;
  effort?: string;
  url?: string;
}

class TaskService {
  private apiBaseUrl = 'http://localhost:8000';  // Make sure this matches your backend URL

  async getAllTasks(): Promise<Task[]> {
    try {
      console.log('Fetching tasks from API...');
      const response = await fetch(`${this.apiBaseUrl}/api/tasks`);
      if (!response.ok) {
        throw new Error('Failed to fetch tasks');
      }
      const tasks = await response.json();
      console.log('Fetched tasks:', tasks);
      return tasks;
    } catch (error) {
      console.error('Error fetching tasks:', error);
      throw error;
    }
  }

  async addTask(task: Omit<Task, 'id'>): Promise<Task> {
    const response = await fetch(`${this.apiBaseUrl}/api/tasks`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(task),
    });

    if (!response.ok) {
      throw new Error('Failed to add task');
    }

    return response.json();
  }

  async updateTask(taskId: string, updates: Partial<Task>): Promise<Task> {
    const response = await fetch(`${this.apiBaseUrl}/api/tasks/${taskId}/properties`, {
      method: 'PATCH',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(updates),
    });

    if (!response.ok) {
      throw new Error('Failed to update task');
    }

    return response.json();
  }

  async deleteTask(taskId: string): Promise<void> {
    const response = await fetch(`${this.apiBaseUrl}/api/tasks/${taskId}`, {
      method: 'DELETE',
    });

    if (!response.ok) {
      throw new Error('Failed to delete task');
    }
  }
}

export const taskService = new TaskService();
