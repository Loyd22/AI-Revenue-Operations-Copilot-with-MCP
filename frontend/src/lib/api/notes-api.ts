import { getAccessToken } from "@/lib/auth/auth-storage";
import type { ApiSuccessResponse, Note } from "@/types/note";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL;

function getAuthHeaders(): HeadersInit {
  const token = getAccessToken();

  return {
    "Content-Type": "application/json",
    Authorization: `Bearer ${token}`,
  };
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

function getErrorMessage(errorData: unknown): string {
  if (
    typeof errorData === "object" &&
    errorData !== null &&
    "detail" in errorData &&
    typeof (errorData as { detail?: unknown }).detail === "string"
  ) {
    return (errorData as { detail: string }).detail;
  }

  return "Something went wrong.";
}

export async function getNotes(): Promise<Note[]> {
  const response = await fetch(`${API_BASE_URL}/notes`, {
    method: "GET",
    headers: getAuthHeaders(),
    cache: "no-store",
  });

  const data = (await parseJsonSafely(response)) as
    | ApiSuccessResponse<Note[]>
    | unknown;

  if (!response.ok) {
    throw new Error(getErrorMessage(data));
  }

  return (data as ApiSuccessResponse<Note[]>).data;
}