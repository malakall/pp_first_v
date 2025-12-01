import React, { createContext, useContext, useEffect, useState } from "react";
import { apiGet, apiPostJson, apiPostVoid } from "./api";

export interface User {
  id: number;
  email: string;
  // сюда можно потом добавить другие поля из модели Users
}

interface AuthContextType {
  user: User | null;
  loading: boolean;
  register: (email: string, password: string) => Promise<void>;
  login: (email: string, password: string) => Promise<void>;
  logout: () => Promise<void>;
}

const AuthContext = createContext<AuthContextType | null>(null);

export const useAuth = () => {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("AuthContext not found");
  return ctx;
};

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    (async () => {
      try {
        const u = await apiGet("/auth/me");
        setUser(u as User);
      } catch {
        setUser(null);
      } finally {
        setLoading(false);
      }
    })();
  }, []);

  const register = async (email: string, password: string) => {
    await apiPostJson("/auth/register", { email, password });
    await login(email, password);
  };

  const login = async (email: string, password: string) => {
    await apiPostJson("/auth/login", { email, password });
    const u = await apiGet("/auth/me");
    setUser(u as User);
  };

  const logout = async () => {
    await apiPostVoid("/auth/logout");
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ user, loading, register, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
};
