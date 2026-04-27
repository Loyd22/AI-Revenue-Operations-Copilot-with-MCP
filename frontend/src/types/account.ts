// These are the frontend types for account data.
// We keep them separate so components and API files can reuse them.

export interface Account {
  id: number;
  name: string;
  industry: string | null;
  company_size: string | null;
  status: string;
  health_status: string | null;
  renewal_date: string | null;
  owner_user_id: number | null;
}

export interface AccountCreateRequest {
  name: string;
  industry?: string | null;
  company_size?: string | null;
  status?: string;
  health_status?: string | null;
  renewal_date?: string | null;
  owner_user_id?: number | null;
}

export interface AccountUpdateRequest {
  name?: string;
  industry?: string | null;
  company_size?: string | null;
  status?: string;
  health_status?: string | null;
  renewal_date?: string | null;
  owner_user_id?: number | null;
}

export interface ApiSuccessResponse<T> {
  success: true;
  message: string;
  data: T;
}