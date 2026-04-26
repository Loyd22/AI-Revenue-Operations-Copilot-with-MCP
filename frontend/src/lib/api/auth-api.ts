// This file talks to the backend auth endpoints.
// It should only handle HTTP requests and responses.

import type {
  ApiSuccessResponse,
  AuthUser,
  LoginRequest,
  LoginResponseData,
  RefreshResponseData,
  RegisterRequest,
} from "@/types/auth";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL;

function getErrorMessage(errorData: unknown): string {
  if (
    typeof errorData === "object" &&
    errorData !== null &&
    "detail" in errorData &&
    typeof (errorData as { detail?: unknown }).detail === "string"
  ) {
    return (errorData as { detail: string }).detail;
  }

  if (
    typeof errorData === "object" &&
    errorData !== null &&
    "message" in errorData &&
    typeof (errorData as { message?: unknown }).message === "string"
  ) {
    return (errorData as { message: string }).message;
  }

  return "Something went wrong.";
}

async function parseJsonSafely(response: Response): Promise<unknown> {
  const text = await response.text();
  if (!text) return null;

  try {
    return JSON.parse(text);
  } catch {
    return null;
  }
}

export async function registerUser(payload: RegisterRequest): Promise<AuthUser> {
  const response = await fetch(`${API_BASE_URL}/auth/register`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
  });

  const data = (await parseJsonSafely(response)) as
    | ApiSuccessResponse<AuthUser>
    | unknown;

  if (!response.ok) {
    throw new Error(getErrorMessage(data));
  }

  return (data as ApiSuccessResponse<AuthUser>).data;
}

export async function loginUser(
  payload: LoginRequest
): Promise<LoginResponseData> {
  const response = await fetch(`${API_BASE_URL}/auth/login`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
  });

  const data = (await parseJsonSafely(response)) as
    | ApiSuccessResponse<LoginResponseData>
    | unknown;

  if (!response.ok) {
    throw new Error(getErrorMessage(data));
  }

  return (data as ApiSuccessResponse<LoginResponseData>).data;
}

export async function getCurrentUser(accessToken: string): Promise<AuthUser> {
  const response = await fetch(`${API_BASE_URL}/auth/me`, {
    method: "GET",
    headers: {
      Authorization: `Bearer ${accessToken}`,
    },
  });

  const data = (await parseJsonSafely(response)) as
    | ApiSuccessResponse<AuthUser>
    | unknown;

  if (!response.ok) {
    throw new Error(getErrorMessage(data));
  }

  return (data as ApiSuccessResponse<AuthUser>).data;
}

export async function refreshAccessToken(
  refreshToken: string
): Promise<RefreshResponseData> {
  const response = await fetch(`${API_BASE_URL}/auth/refresh`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      refresh_token: refreshToken,
    }),
  });

  const data = (await parseJsonSafely(response)) as
    | ApiSuccessResponse<RefreshResponseData>
    | unknown;

  if (!response.ok) {
    throw new Error(getErrorMessage(data));
  }

  return (data as ApiSuccessResponse<RefreshResponseData>).data;
}