"use client";

import { useEffect, useState } from "react";

import { getDashboardData } from "@/lib/api/dashboard-api";
import type { DashboardData } from "@/types/dashboard";
import { MetricCards } from "@/features/dashboard/components/metric-cards";
import { RecentSection } from "@/features/dashboard/components/recent-section";

export function DashboardOverview() {
  const [dashboard, setDashboard] = useState<DashboardData | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [errorMessage, setErrorMessage] = useState("");

  useEffect(() => {
    async function loadDashboard() {
      try {
        setIsLoading(true);
        setErrorMessage("");

        const data = await getDashboardData();
        setDashboard(data);
      } catch (error) {
        setErrorMessage(
          error instanceof Error ? error.message : "Failed to load dashboard."
        );
      } finally {
        setIsLoading(false);
      }
    }

    void loadDashboard();
  }, []);

  if (isLoading) {
    return <p>Loading dashboard...</p>;
  }

  if (errorMessage) {
    return <p className="text-red-600">{errorMessage}</p>;
  }

  if (!dashboard) {
    return <p>No dashboard data found.</p>;
  }

  return (
    <div className="space-y-6">
      <MetricCards
        totalAccounts={dashboard.total_accounts}
        totalDeals={dashboard.total_deals}
        totalActivities={dashboard.total_activities}
        totalNotes={dashboard.total_notes}
      />

      <div className="grid gap-6 lg:grid-cols-2">
        <RecentSection
          title="Deals by Risk"
          items={dashboard.deals_by_risk}
          renderItem={(item) => (
            <div className="flex items-center justify-between">
              <p className="font-medium">{item.label}</p>
              <p>{item.value}</p>
            </div>
          )}
        />

        <RecentSection
          title="Deals by Status"
          items={dashboard.deals_by_status}
          renderItem={(item) => (
            <div className="flex items-center justify-between">
              <p className="font-medium">{item.label}</p>
              <p>{item.value}</p>
            </div>
          )}
        />
      </div>

      <div className="grid gap-6 lg:grid-cols-2">
        <RecentSection
          title="Recent Accounts"
          items={dashboard.recent_accounts}
          renderItem={(item) => (
            <div>
              <p className="font-medium">{item.name}</p>
              <p className="text-sm text-gray-600">
                {item.industry ?? "No industry"} • {item.status}
              </p>
            </div>
          )}
        />

        <RecentSection
          title="Recent Deals"
          items={dashboard.recent_deals}
          renderItem={(item) => (
            <div>
              <p className="font-medium">{item.title}</p>
              <p className="text-sm text-gray-600">
                {item.status} • Risk: {item.risk_level ?? "N/A"}
              </p>
            </div>
          )}
        />

        <RecentSection
          title="Recent Activities"
          items={dashboard.recent_activities}
          renderItem={(item) => (
            <div>
              <p className="font-medium">{item.subject}</p>
              <p className="text-sm text-gray-600">
                {item.activity_type} • {item.status}
              </p>
            </div>
          )}
        />

        <RecentSection
          title="Recent Notes"
          items={dashboard.recent_notes}
          renderItem={(item) => (
            <div>
              <p className="font-medium">{item.note_type}</p>
              <p className="text-sm text-gray-600 line-clamp-2">{item.content}</p>
            </div>
          )}
        />
      </div>
    </div>
  );
}