export interface Activity {
  id: number;
  account_id: number;
  deal_id: number | null;
  user_id: number | null;
  activity_type: string;
  subject: string;
  activity_at: string;
  status: string;
  summary: string | null;
}

export interface ApiSuccessResponse<T> {
  success: true;
  message: string;
  data: T;
}