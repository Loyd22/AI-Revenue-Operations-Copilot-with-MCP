"use client";

// This file creates the global auth context for the frontend.
// It stores the current user, handles login/signup/logout,
// and restores auth state when the app loads.

import {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useMemo,
  useState,
  type ReactNode,
} from "react";

import { getCurrentUser, loginUser, refreshAccessToken, registerUser } from "@/lib/api/auth-api";
import {
  clearTokens,
  getAccessToken,
  getRefreshToken,
  setTokens,
} from "@/lib/auth/auth-storage";
import type {
  AuthContextValue,
  AuthUser,
  LoginRequest,
  RegisterRequest,
} from "@/types/auth";

const AuthContext = createContext<AuthContextValue | undefined>(undefined);

interface AuthProviderProps {
  children: ReactNode;
}

export function AuthProvider({ children }: AuthProviderProps) {
  const [user, setUser] = useState<AuthUser | null>(null);
  const [accessToken, setAccessTokenState] = useState<string | null>(null);
  const [refreshToken, setRefreshTokenState] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  const logout = useCallback(() => {
    clearTokens();
    setUser(null);
    setAccessTokenState(null);
    setRefreshTokenState(null);
  }, []);

  const fetchCurrentUser = useCallback(async () => {
    const storedAccessToken = getAccessToken();
    const storedRefreshToken = getRefreshToken();

    if (!storedAccessToken) {
      setIsLoading(false);
      return;
    }

    try {
      const currentUser = await getCurrentUser(storedAccessToken);
      setUser(currentUser);
      setAccessTokenState(storedAccessToken);
      setRefreshTokenState(storedRefreshToken);
    } catch {
      // If access token expired, try refresh token.
      if (!storedRefreshToken) {
        logout();
        setIsLoading(false);
        return;
      }

      try {
        const refreshed = await refreshAccessToken(storedRefreshToken);
        setTokens(refreshed.access_token, storedRefreshToken);
        setAccessTokenState(refreshed.access_token);
        setRefreshTokenState(storedRefreshToken);

        const currentUser = await getCurrentUser(refreshed.access_token);
        setUser(currentUser);
      } catch {
        logout();
      }
    } finally {
      setIsLoading(false);
    }
  }, [logout]);

  const login = useCallback(async (payload: LoginRequest) => {
    const data = await loginUser(payload);

    setTokens(data.access_token, data.refresh_token);
    setAccessTokenState(data.access_token);
    setRefreshTokenState(data.refresh_token);
    setUser(data.user);
  }, []);

  const signup = useCallback(async (payload: RegisterRequest) => {
    // First create the user.
    await registerUser(payload);

    // Then automatically log in the new user.
    const loginData = await loginUser({
      email: payload.email,
      password: payload.password,
    });

    setTokens(loginData.access_token, loginData.refresh_token);
    setAccessTokenState(loginData.access_token);
    setRefreshTokenState(loginData.refresh_token);
    setUser(loginData.user);
  }, []);

  useEffect(() => {
    void fetchCurrentUser();
  }, [fetchCurrentUser]);

  const value = useMemo<AuthContextValue>(
    () => ({
      user,
      accessToken,
      refreshToken,
      isAuthenticated: Boolean(user && accessToken),
      isLoading,
      login,
      signup,
      logout,
      fetchCurrentUser,
    }),
    [user, accessToken, refreshToken, isLoading, login, signup, logout, fetchCurrentUser]
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth(): AuthContextValue {
  const context = useContext(AuthContext);

  if (!context) {
    throw new Error("useAuth must be used inside AuthProvider");
  }

  return context;
}