export interface Note {
  id: number;
  account_id: number;
  deal_id: number | null;
  user_id: number | null;
  note_type: string;
  content: string;
  source: string;
}

export interface ApiSuccessResponse<T> {
  success: true;
  message: string;
  data: T;
}