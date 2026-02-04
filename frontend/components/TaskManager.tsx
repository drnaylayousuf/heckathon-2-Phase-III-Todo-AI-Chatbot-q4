"use client";

import { useState, useEffect } from "react";
import { Task, TaskStatus, TaskPriority } from "@/types/task";

interface TaskManagerProps {
  userId?: string; // Make it optional since we'll get the user ID from the auth token
}

const TaskManager = ({ userId }: TaskManagerProps) => {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [newTask, setNewTask] = useState({ title: "", description: "", priority: "medium" as TaskPriority });
  const [editingTask, setEditingTask] = useState<Task | null>(null);
  const [filter, setFilter] = useState<{ status?: TaskStatus; priority?: TaskPriority }>({});

  // Get user ID from the JWT token
  const getUserIdFromToken = (): string | null => {
    const token = localStorage.getItem("accessToken");
    if (!token) return null;

    try {
      const payload = token.split('.')[1];
      const decodedPayload = atob(payload);
      const parsedPayload = JSON.parse(decodedPayload);
      return parsedPayload.user_id || null;
    } catch (error) {
      console.error("Error decoding token:", error);
      return null;
    }
  };

  // Load tasks - refresh when token becomes available
  useEffect(() => {
    const timer = setTimeout(() => {
      fetchTasks();
    }, 500); // Small delay to ensure token is available

    return () => clearTimeout(timer);
  }, []);

  const fetchTasks = async () => {
    const token = localStorage.getItem("accessToken");
    if (!token) {
      setError("No access token found");
      setLoading(false);
      return;
    }

    const actualUserId = userId || getUserIdFromToken();
    if (!actualUserId) {
      setError("Unable to determine user ID from token");
      setLoading(false);
      return;
    }

    try {
      setLoading(true);

      // Test the connection first
      const testResponse = await fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL || 'https://nayla-yousuf-123-todo-app-chatbot-phase3.hf.space'}/health`);
      if (!testResponse.ok) {
        throw new Error("Cannot reach the API server");
      }

      const response = await fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL || 'https://nayla-yousuf-123-todo-app-chatbot-phase3.hf.space'}/api/${actualUserId}/tasks`, {
        headers: {
          "Authorization": `Bearer ${token}`,
          "Content-Type": "application/json",
        },
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        if (response.status === 401) {
          setError("Authentication failed. Please log in again.");
        } else if (response.status === 403) {
          setError("Access denied. You don't have permission to view these tasks.");
        } else if (response.status === 404) {
          setError("Tasks endpoint not found. Please contact support.");
        } else {
          throw new Error(errorData.detail || `Failed to fetch tasks: ${response.status}`);
        }
      } else {
        const data = await response.json();
        setTasks(data);
      }
    } catch (err) {
      console.error("Fetch tasks error:", err);
      if (err instanceof TypeError && (err.message.includes('fetch') || err.message.includes('network'))) {
        setError("Network error. Please check that the backend server is running on http://127.0.0.1:8000.");
      } else {
        setError(`Connection error: ${(err as Error).message}`);
      }
    } finally {
      setLoading(false);
    }
  };

  const handleAddTask = async (e: React.FormEvent) => {
    e.preventDefault();
    const actualUserId = userId || getUserIdFromToken();
    if (!actualUserId) {
      setError("User not authenticated");
      return;
    }

    try {
      const accessToken = localStorage.getItem("accessToken");
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL || 'https://nayla-yousuf-123-todo-app-chatbot-phase3.hf.space'}/api/${actualUserId}/tasks`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Authorization": `Bearer ${accessToken}`,
        },
        body: JSON.stringify({
          title: newTask.title,
          description: newTask.description,
          priority: newTask.priority,
        }),
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || "Failed to add task");
      }

      const createdTask = await response.json();
      setTasks([...tasks, createdTask]);
      setNewTask({ title: "", description: "", priority: "medium" as TaskPriority });
    } catch (err) {
      setError((err as Error).message);
    }
  };

  const handleUpdateTask = async () => {
    if (!editingTask) return;
    const actualUserId = userId || getUserIdFromToken();
    if (!actualUserId) {
      setError("User not authenticated");
      return;
    }

    try {
      const accessToken = localStorage.getItem("accessToken");
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL || 'https://nayla-yousuf-123-todo-app-chatbot-phase3.hf.space'}/api/${actualUserId}/tasks/${editingTask.id}`, {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
          "Authorization": `Bearer ${accessToken}`,
        },
        body: JSON.stringify({
          title: editingTask.title,
          description: editingTask.description,
          priority: editingTask.priority,
        }),
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || "Failed to update task");
      }

      const updatedTask = await response.json();
      setTasks(tasks.map(t => t.id === editingTask.id ? updatedTask : t));
      setEditingTask(null);
    } catch (err) {
      setError((err as Error).message);
    }
  };

  const handleToggleComplete = async (task: Task) => {
    const actualUserId = userId || getUserIdFromToken();
    if (!actualUserId) {
      setError("User not authenticated");
      return;
    }

    try {
      const accessToken = localStorage.getItem("accessToken");
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL || 'https://nayla-yousuf-123-todo-app-chatbot-phase3.hf.space'}/api/${actualUserId}/tasks/${task.id}/complete`, {
        method: "PATCH",
        headers: {
          "Content-Type": "application/json",
          "Authorization": `Bearer ${accessToken}`,
        },
        body: JSON.stringify({
          completed: task.status !== "completed",
        }),
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || "Failed to update task status");
      }

      const updatedTask = await response.json();
      setTasks(tasks.map(t => t.id === task.id ? updatedTask : t));
    } catch (err) {
      setError((err as Error).message);
    }
  };

  const handleDeleteTask = async (taskId: string) => {
    const actualUserId = userId || getUserIdFromToken();
    if (!actualUserId) {
      setError("User not authenticated");
      return;
    }

    try {
      const accessToken = localStorage.getItem("accessToken");
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL || 'https://nayla-yousuf-123-todo-app-chatbot-phase3.hf.space'}/api/${actualUserId}/tasks/${taskId}`, {
        method: "DELETE",
        headers: {
          "Authorization": `Bearer ${accessToken}`,
        },
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || "Failed to delete task");
      }

      setTasks(tasks.filter(t => t.id !== taskId));
    } catch (err) {
      setError((err as Error).message);
    }
  };

  const filteredTasks = tasks.filter(task => {
    if (filter.status && task.status !== filter.status) return false;
    if (filter.priority && task.priority !== filter.priority) return false;
    return true;
  });

  if (loading) {
    return (
      <div className="flex justify-center items-center h-32">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-indigo-600"></div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="rounded-md bg-red-50 p-4">
        <div className="text-sm text-red-700">{error}</div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Add Task Form */}
      <form onSubmit={handleAddTask} className="space-y-4">
        <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
          <div>
            <label htmlFor="title" className="block text-sm font-medium text-gray-700">
              Task Title
            </label>
            <input
              type="text"
              id="title"
              value={newTask.title}
              onChange={(e) => setNewTask({...newTask, title: e.target.value})}
              className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
              placeholder="What needs to be done?"
              required
            />
          </div>
          <div>
            <label htmlFor="priority" className="block text-sm font-medium text-gray-700">
              Priority
            </label>
            <select
              id="priority"
              value={newTask.priority}
              onChange={(e) => setNewTask({...newTask, priority: e.target.value as TaskPriority})}
              className="mt-1 block w-full bg-white border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
            >
              <option value="low">Low</option>
              <option value="medium">Medium</option>
              <option value="high">High</option>
            </select>
          </div>
        </div>
        <div>
          <label htmlFor="description" className="block text-sm font-medium text-gray-700">
            Description (Optional)
          </label>
          <textarea
            id="description"
            rows={2}
            value={newTask.description}
            onChange={(e) => setNewTask({...newTask, description: e.target.value})}
            className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
            placeholder="Add details..."
          />
        </div>
        <button
          type="submit"
          className="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
        >
          Add Task
        </button>
      </form>

      {/* Filters */}
      <div className="flex space-x-4">
        <select
          value={filter.status || ""}
          onChange={(e) => setFilter({...filter, status: e.target.value as TaskStatus || undefined})}
          className="block w-full bg-white border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
        >
          <option value="">All Statuses</option>
          <option value="pending">Pending</option>
          <option value="in-progress">In Progress</option>
          <option value="completed">Completed</option>
        </select>
        <select
          value={filter.priority || ""}
          onChange={(e) => setFilter({...filter, priority: e.target.value as TaskPriority || undefined})}
          className="block w-full bg-white border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
        >
          <option value="">All Priorities</option>
          <option value="low">Low</option>
          <option value="medium">Medium</option>
          <option value="high">High</option>
        </select>
      </div>

      {/* Task List */}
      <div className="space-y-3">
        {filteredTasks.length === 0 ? (
          <div className="text-center py-8 text-gray-500">
            <p>No tasks found. Add a new task to get started!</p>
          </div>
        ) : (
          filteredTasks.map((task) => (
            <div
              key={task.id}
              className={`border rounded-lg p-4 ${
                task.status === "completed" ? "bg-green-50 border-green-200" : "bg-white border-gray-200"
              }`}
            >
              {editingTask?.id === task.id ? (
                <div className="space-y-3">
                  <input
                    type="text"
                    value={editingTask.title}
                    onChange={(e) => setEditingTask({...editingTask, title: e.target.value})}
                    className="block w-full border border-gray-300 rounded-md shadow-sm py-1 px-2 text-sm"
                  />
                  <textarea
                    value={editingTask.description || ""}
                    onChange={(e) => setEditingTask({...editingTask, description: e.target.value})}
                    className="block w-full border border-gray-300 rounded-md shadow-sm py-1 px-2 text-sm"
                  />
                  <select
                    value={editingTask.priority}
                    onChange={(e) => setEditingTask({...editingTask, priority: e.target.value as TaskPriority})}
                    className="block w-full border border-gray-300 rounded-md shadow-sm py-1 px-2 text-sm"
                  >
                    <option value="low">Low</option>
                    <option value="medium">Medium</option>
                    <option value="high">High</option>
                  </select>
                  <div className="flex space-x-2">
                    <button
                      onClick={handleUpdateTask}
                      className="px-3 py-1 bg-green-600 text-white text-sm rounded hover:bg-green-700"
                    >
                      Save
                    </button>
                    <button
                      onClick={() => setEditingTask(null)}
                      className="px-3 py-1 bg-gray-600 text-white text-sm rounded hover:bg-gray-700"
                    >
                      Cancel
                    </button>
                  </div>
                </div>
              ) : (
                <div className="flex items-start justify-between">
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center">
                      <input
                        type="checkbox"
                        checked={task.status === "completed"}
                        onChange={() => handleToggleComplete(task)}
                        className="h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded"
                      />
                      <span
                        className={`ml-3 text-sm font-medium ${
                          task.status === "completed" ? "text-gray-500 line-through" : "text-gray-900"
                        }`}
                      >
                        {task.title}
                      </span>
                    </div>
                    {task.description && (
                      <p className="ml-7 mt-1 text-sm text-gray-500">{task.description}</p>
                    )}
                    <div className="ml-7 mt-2 flex items-center space-x-4">
                      <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                        task.priority === 'high' ? 'bg-red-100 text-red-800' :
                        task.priority === 'medium' ? 'bg-yellow-100 text-yellow-800' :
                        'bg-green-100 text-green-800'
                      }`}>
                        {task.priority}
                      </span>
                      <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                        task.status === 'completed' ? 'bg-green-100 text-green-800' :
                        task.status === 'in-progress' ? 'bg-blue-100 text-blue-800' :
                        'bg-gray-100 text-gray-800'
                      }`}>
                        {task.status.replace('-', ' ')}
                      </span>
                      {task.dueDate && (
                        <span className="text-xs text-gray-500">
                          Due: {new Date(task.dueDate).toLocaleDateString()}
                        </span>
                      )}
                    </div>
                  </div>
                  <div className="flex space-x-2 ml-4">
                    <button
                      onClick={() => setEditingTask(task)}
                      className="text-indigo-600 hover:text-indigo-900 text-sm font-medium"
                    >
                      Edit
                    </button>
                    <button
                      onClick={() => handleDeleteTask(task.id)}
                      className="text-red-600 hover:text-red-900 text-sm font-medium"
                    >
                      Delete
                    </button>
                  </div>
                </div>
              )}
            </div>
          ))
        )}
      </div>
    </div>
  );
};

export default TaskManager;