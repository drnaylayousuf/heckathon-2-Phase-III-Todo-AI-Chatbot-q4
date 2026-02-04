"use client";

import { createContext, useContext, useState, useEffect, ReactNode } from "react";
import axios from "axios";

// Define types
interface User {
  id: string;
  email: string;
  name?: string;
  createdAt: string;
  updatedAt: string;
  isActive: boolean;
}

interface AuthContextType {
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  signIn: (email: string, password: string) => Promise<void>;
  signOut: () => void;
  signUp: (email: string, password: string, name?: string) => Promise<void>;
}

// Create context
const AuthContext = createContext<AuthContextType | undefined>(undefined);

// Auth provider component
export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(true);

  // Check if user is authenticated on initial load
  useEffect(() => {
    const token = localStorage.getItem("accessToken");
    if (token) {
      // Verify token and get user info
      verifyTokenAndLoadUser(token);
    } else {
      setIsLoading(false);
    }
  }, []);

  const verifyTokenAndLoadUser = async (token: string) => {
    try {
      // Set the auth token for axios
      axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;

      // Get user info
      const response = await axios.get(`${process.env.NEXT_PUBLIC_API_BASE_URL || 'https://nayla-yousuf-123-todo-app-chatbot-phase3.hf.space'}/api/me`);
      setUser(response.data);
    } catch (error) {
      // Token is invalid, clear it
      localStorage.removeItem("accessToken");
      delete axios.defaults.headers.common['Authorization'];
    } finally {
      setIsLoading(false);
    }
  };

  const signIn = async (email: string, password: string) => {
    try {
      // Create form data for the login request (required by OAuth2PasswordRequestForm)
      const formData = new FormData();
      formData.append('username', email);
      formData.append('password', password);

      const response = await axios.post(`${process.env.NEXT_PUBLIC_API_BASE_URL || 'https://nayla-yousuf-123-todo-app-chatbot-phase3.hf.space'}/api/login`,
        formData,
        {
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
          }
        }
      );

      const { access_token } = response.data;
      localStorage.setItem("accessToken", access_token);

      // Set the auth token for axios
      axios.defaults.headers.common['Authorization'] = `Bearer ${access_token}`;

      // Get user info
      const userInfoResponse = await axios.get(`${process.env.NEXT_PUBLIC_API_BASE_URL || 'https://nayla-yousuf-123-todo-app-chatbot-phase3.hf.space'}/api/me`);
      setUser(userInfoResponse.data);
    } catch (error) {
      if (axios.isAxiosError(error)) {
        throw new Error(error.response?.data?.detail || "Invalid credentials");
      }
      throw new Error("Invalid credentials");
    }
  };

  const signOut = () => {
    localStorage.removeItem("accessToken");
    delete axios.defaults.headers.common['Authorization'];
    setUser(null);
  };

  const signUp = async (email: string, password: string, name?: string) => {
    try {
      await axios.post(`${process.env.NEXT_PUBLIC_API_BASE_URL || 'https://nayla-yousuf-123-todo-app-chatbot-phase3.hf.space'}/api/register`, {
        email,
        password,
        name,
      });

      // After successful registration, the user should be redirected to login
      // Automatic login may fail if the user needs to be activated or if there's a delay
      // So we'll just return successfully and let the UI handle the redirect
    } catch (error) {
      if (axios.isAxiosError(error)) {
        // Try to get more specific error message from the backend
        const errorMessage = error.response?.data?.detail || "Registration failed";
        throw new Error(errorMessage);
      }
      throw new Error("Registration failed");
    }
  };

  const value = {
    user,
    isAuthenticated: !!user,
    isLoading,
    signIn,
    signOut,
    signUp,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

// Custom hook to use auth context
export function useAuth() {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error("useAuth must be used within an AuthProvider");
  }
  return context;
}