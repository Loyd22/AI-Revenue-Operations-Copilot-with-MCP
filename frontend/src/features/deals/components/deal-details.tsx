"use client";

import { useEffect, useState } from "react";

import { getDealById } from "@/lib/api/deals-api";
import type { Deal } from "@/types/deal";

interface DealDetailsProps {
  dealId: number;
}

export function DealDetails({ dealId }: DealDetailsProps) {
  const [deal, setDeal] = useState<Deal | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [errorMessage, setErrorMessage] = useState("");

  useEffect(() => {
    async function loadDeal() {
      try {
        setIsLoading(true);
        setErrorMessage("");
        const data = await getDealById(dealId);
        setDeal(data);
      } catch (error) {
        setErrorMessage(
          error instanceof Error ? error.message : "Failed to load deal."
        );
      } finally {
        setIsLoading(false);
      }
    }

    void loadDeal();
  }, [dealId]);

  if (isLoading) return <p>Loading deal...</p>;
  if (errorMessage) return <p className="text-red-600">{errorMessage}</p>;
  if (!deal) return <p>Deal not found.</p>;

  return (
    <div className="rounded-2xl bg-white p-8 shadow-sm">
      <h1 className="text-2xl font-semibold">{deal.title}</h1>

      <div className="mt-6 grid gap-4 sm:grid-cols-2">
        <div className="rounded-xl border p-4">
          <p className="text-sm text-gray-500">Account ID</p>
          <p className="font-medium">{deal.account_id}</p>
        </div>

        <div className="rounded-xl border p-4">
          <p className="text-sm text-gray-500">Owner User ID</p>
          <p className="font-medium">{deal.owner_user_id ?? "N/A"}</p>
        </div>

        <div className="rounded-xl border p-4">
          <p className="text-sm text-gray-500">Stage ID</p>
          <p className="font-medium">{deal.stage_id ?? "N/A"}</p>
        </div>

        <div className="rounded-xl border p-4">
          <p className="text-sm text-gray-500">Amount</p>
          <p className="font-medium">{deal.amount ?? "N/A"}</p>
        </div>

        <div className="rounded-xl border p-4">
          <p className="text-sm text-gray-500">Status</p>
          <p className="font-medium">{deal.status}</p>
        </div>

        <div className="rounded-xl border p-4">
          <p className="text-sm text-gray-500">Risk Level</p>
          <p className="font-medium">{deal.risk_level ?? "N/A"}</p>
        </div>

        <div className="rounded-xl border p-4">
          <p className="text-sm text-gray-500">Expected Close Date</p>
          <p className="font-medium">{deal.expected_close_date ?? "N/A"}</p>
        </div>

        <div className="rounded-xl border p-4">
          <p className="text-sm text-gray-500">Last Activity At</p>
          <p className="font-medium">{deal.last_activity_at ?? "N/A"}</p>
        </div>
      </div>
    </div>
  );
}