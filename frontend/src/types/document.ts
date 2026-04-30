export interface DocumentItem {
  id: number;
  title: string;
  file_name: string;
  storage_path: string;
  document_type: string;
  status: string;
  uploaded_by_user_id: number | null;
}

export interface ApiSuccessResponse<T> {
  success: true;
  message: string;
  data: T;
}