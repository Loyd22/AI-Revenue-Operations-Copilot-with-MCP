"use client";

import Link from "next/link";
import { useEffect, useState } from "react";

import { getDeals } from "@/lib/api/deals-api";
import type { Deal } from "@/types/deal";

export function DealsList() {
  const [deals, setDeals] = useState<Deal[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [errorMessage, setErrorMessage] = useState("");

  useEffect(() => {
    async function loadDeals() {
      try {
        setIsLoading(true);
        setErrorMessage("");
        const data = await getDeals();
        setDeals(data);
      } catch (error) {
        setErrorMessage(
          error instanceof Error ? error.message : "Failed to load deals."
        );
      } finally {
        setIsLoading(false);
      }
    }

    void loadDeals();
  }, []);

  if (isLoading) return <p>Loading deals...</p>;
  if (errorMessage) return <p className="text-red-600">{errorMessage}</p>;
  if (deals.length === 0) return <p>No deals found.</p>;

  return (
    <div className="space-y-4">
      {deals.map((deal) => (
        <Link
          key={deal.id}
          href={`/deals/${deal.id}`}
          className="block rounded-xl border bg-white p-4 shadow-sm transition hover:shadow"
        >
          <div className="flex items-center justify-between gap-4">
            <div>
              <h2 className="text-lg font-semibold">{deal.title}</h2>
              <p className="text-sm text-gray-600">
                Account ID: {deal.account_id} • Stage ID: {deal.stage_id ?? "N/A"}
              </p>
            </div>

            <div className="text-right text-sm">
              <p>
                <span className="font-medium">Status:</span> {deal.status}
              </p>
              <p>
                <span className="font-medium">Risk:</span> {deal.risk_level ?? "N/A"}
              </p>
            </div>
          </div>
        </Link>
      ))}
    </div>
  );
}