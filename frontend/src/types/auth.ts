// These are the shared TypeScript types for auth-related data.
// Keeping them here makes the frontend easier to maintain.

export type UserRole =
  | "admin"
  | "sales_rep"
  | "account_manager"
  | "revops_manager"
  | "sales_director";

export interface AuthUser {
  id: number;
  full_name: string;
  email: string;
  role: UserRole;
}

export interface LoginRequest {
  email: string;
  password: string;
}

export interface RegisterRequest {
  full_name: string;
  email: string;
  password: string;
  role: UserRole;
}

export interface RefreshTokenRequest {
  refresh_token: string;
}

export interface LoginResponseData {
  access_token: string;
  refresh_token: string;
  token_type: string;
  user: AuthUser;
}

export interface RefreshResponseData {
  access_token: string;
  token_type: string;
}

export interface ApiSuccessResponse<T> {
  success: true;
  message: string;
  data: T;
}

export interface ApiErrorResponse {
  detail?: string;
  message?: string;
  error?: {
    code?: string;
    details?: unknown;
  };
}

export interface AuthContextValue {
  user: AuthUser | null;
  accessToken: string | null;
  refreshToken: string | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  login: (payload: LoginRequest) => Promise<void>;
  signup: (payload: RegisterRequest) => Promise<void>;
  logout: () => void;
  fetchCurrentUser: () => Promise<void>;
}