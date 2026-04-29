"use client";

import { useEffect, useState } from "react";

import { getActivities } from "@/lib/api/activities-api";
import type { Activity } from "@/types/activity";

export function ActivitiesList() {
  const [activities, setActivities] = useState<Activity[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [errorMessage, setErrorMessage] = useState("");

  useEffect(() => {
    async function loadActivities() {
      try {
        setIsLoading(true);
        setErrorMessage("");
        const data = await getActivities();
        setActivities(data);
      } catch (error) {
        setErrorMessage(
          error instanceof Error ? error.message : "Failed to load activities."
        );
      } finally {
        setIsLoading(false);
      }
    }

    void loadActivities();
  }, []);

  if (isLoading) return <p>Loading activities...</p>;
  if (errorMessage) return <p className="text-red-600">{errorMessage}</p>;
  if (activities.length === 0) return <p>No activities found.</p>;

  return (
    <div className="space-y-4">
      {activities.map((activity) => (
        <div key={activity.id} className="rounded-xl border bg-white p-4 shadow-sm">
          <h2 className="text-lg font-semibold">{activity.subject}</h2>
          <p className="text-sm text-gray-600">
            {activity.activity_type} • {activity.status}
          </p>
          <p className="mt-2 text-sm">Account ID: {activity.account_id}</p>
          <p className="text-sm">Deal ID: {activity.deal_id ?? "N/A"}</p>
          <p className="text-sm">At: {activity.activity_at}</p>
          <p className="mt-2 text-sm text-gray-700">
            {activity.summary ?? "No summary"}
          </p>
        </div>
      ))}
    </div>
  );
}