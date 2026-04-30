import { getAccessToken } from "@/lib/auth/auth-storage";
import type { ApiSuccessResponse, DocumentItem } from "@/types/document";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL;

function getAuthHeaders(includeJson = true): HeadersInit {
  const token = getAccessToken();

  return includeJson
    ? {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      }
    : {
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

export async function getDocuments(): Promise<DocumentItem[]> {
  const response = await fetch(`${API_BASE_URL}/documents`, {
    method: "GET",
    headers: getAuthHeaders(),
    cache: "no-store",
  });

  const data = (await parseJsonSafely(response)) as
    | ApiSuccessResponse<DocumentItem[]>
    | unknown;

  if (!response.ok) {
    throw new Error(getErrorMessage(data));
  }

  return (data as ApiSuccessResponse<DocumentItem[]>).data;
}

export async function uploadDocument(
  title: string,
  documentType: string,
  file: File
): Promise<DocumentItem> {
  const formData = new FormData();
  formData.append("title", title);
  formData.append("document_type", documentType);
  formData.append("file", file);

  const response = await fetch(`${API_BASE_URL}/documents`, {
    method: "POST",
    headers: getAuthHeaders(false),
    body: formData,
  });

  const data = (await parseJsonSafely(response)) as
    | ApiSuccessResponse<DocumentItem>
    | unknown;

  if (!response.ok) {
    throw new Error(getErrorMessage(data));
  }

  return (data as ApiSuccessResponse<DocumentItem>).data;
}