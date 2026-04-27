export interface Deal {
  id: number;
  account_id: number;
  owner_user_id: number | null;
  stage_id: number | null;
  title: string;
  amount: string | null;
  status: string;
  risk_level: string | null;
  expected_close_date: string | null;
  last_activity_at: string | null;
}

export interface ApiSuccessResponse<T> {
  success: true;
  message: string;
  data: T;
}