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
      const response = await axios.get(`${process.env.NEXT_PUBLIC_API_BASE_URL || 'https://nayla-yousuf-123-todo-app-chatbot-phase3.hf.space'}/api/auth/me`);
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
      const response = await axios.post(`${process.env.NEXT_PUBLIC_API_BASE_URL || 'https://nayla-yousuf-123-todo-app-chatbot-phase3.hf.space'}/api/auth/login`, {
        username: email,
        password: password,
      });

      const { access_token } = response.data;
      localStorage.setItem("accessToken", access_token);

      // Set the auth token for axios
      axios.defaults.headers.common['Authorization'] = `Bearer ${access_token}`;

      // Get user info
      const userInfoResponse = await axios.get(`${process.env.NEXT_PUBLIC_API_BASE_URL || 'https://nayla-yousuf-123-todo-app-chatbot-phase3.hf.space'}/api/auth/me`);
      setUser(userInfoResponse.data);
    } catch (error) {
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
      await axios.post(`${process.env.NEXT_PUBLIC_API_BASE_URL || 'https://nayla-yousuf-123-todo-app-chatbot-phase3.hf.space'}/api/auth/register`, {
        email,
        password,
        name,
      });

      // Automatically sign in after registration
      await signIn(email, password);
    } catch (error) {
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