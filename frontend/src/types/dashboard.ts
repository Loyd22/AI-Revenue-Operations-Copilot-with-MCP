export interface DashboardMetricItem {
  label: string;
  value: number;
}

export interface DashboardRecentAccountItem {
  id: number;
  name: string;
  industry: string | null;
  status: string;
  health_status: string | null;
}

export interface DashboardRecentDealItem {
  id: number;
  title: string;
  status: string;
  risk_level: string | null;
  account_id: number;
}

export interface DashboardRecentActivityItem {
  id: number;
  subject: string;
  activity_type: string;
  status: string;
  account_id: number;
}

export interface DashboardRecentNoteItem {
  id: number;
  note_type: string;
  content: string;
  account_id: number;
}

export interface DashboardData {
  total_accounts: number;
  total_deals: number;
  total_activities: number;
  total_notes: number;
  deals_by_risk: DashboardMetricItem[];
  deals_by_status: DashboardMetricItem[];
  recent_accounts: DashboardRecentAccountItem[];
  recent_deals: DashboardRecentDealItem[];
  recent_activities: DashboardRecentActivityItem[];
  recent_notes: DashboardRecentNoteItem[];
}

export interface ApiSuccessResponse<T> {
  success: true;
  message: string;
  data: T;
}