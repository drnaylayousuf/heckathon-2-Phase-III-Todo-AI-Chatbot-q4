"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import { useAuth } from "@/hooks/useAuth";
import Link from "next/link";
import TaskManager from "@/components/TaskManager";
import ChatInterface from "@/components/ChatInterface";

export default function DashboardPage() {
  const { user, isAuthenticated, isLoading, signOut } = useAuth();
  const router = useRouter();

  if (isLoading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="animate-spin rounded-full h-32 w-32 border-t-2 border-b-2 border-blue-500"></div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16 items-center">
            <div className="flex items-center">
              <h1 className="text-xl font-semibold text-gray-900">Todo Dashboard</h1>
            </div>
            {isAuthenticated && (
              <div className="flex items-center space-x-4">
                <span className="text-sm text-gray-700">Welcome, {user?.name || user?.email}</span>
                <button
                  onClick={signOut}
                  className="ml-4 px-4 py-2 text-sm font-medium text-white bg-red-600 rounded-md hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500"
                >
                  Sign out
                </button>
              </div>
            )}
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        {!isAuthenticated ? (
          <div className="flex flex-col items-center justify-center">
            <h2 className="text-3xl font-bold text-gray-900 mb-8">Task Management</h2>
            <div className="flex flex-col sm:flex-row gap-4">
              <Link
                href="/login"
                className="px-6 py-3 bg-indigo-600 text-white font-medium rounded-md hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 text-center"
              >
                Sign In
              </Link>
              <Link
                href="/register"
                className="px-6 py-3 bg-white text-gray-700 font-medium rounded-md border border-gray-300 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 text-center"
              >
                Register
              </Link>
            </div>
          </div>
        ) : (
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
            {/* Task Management Panel */}
            <div className="lg:col-span-1">
              <div className="bg-white shadow overflow-hidden sm:rounded-lg">
                <div className="px-4 py-5 sm:px-6 border-b border-gray-200">
                  <h2 className="text-lg leading-6 font-medium text-gray-900">Task Management</h2>
                  <p className="mt-1 text-sm text-gray-500">Create, update, and track your tasks</p>
                </div>
                <div className="px-4 py-5 sm:p-6">
                  {user?.id ? (
                    <TaskManager userId={user.id} />
                  ) : (
                    <div className="text-center py-8 text-gray-500">
                      <p>Loading user information...</p>
                    </div>
                  )}
                </div>
              </div>
            </div>

            {/* AI Chat Panel */}
            <div className="lg:col-span-1">
              <div className="bg-white shadow overflow-hidden sm:rounded-lg">
                <div className="px-4 py-5 sm:px-6 border-b border-gray-200">
                  <h2 className="text-lg leading-6 font-medium text-gray-900">AI Assistant</h2>
                  <p className="mt-1 text-sm text-gray-500">Chat with our AI to manage your tasks</p>
                </div>
                <div className="px-4 py-5 sm:p-6">
                  <ChatInterface userId={user?.id} />
                </div>
              </div>
            </div>
          </div>
        )}
      </main>
    </div>
  );
}