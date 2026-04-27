"use client";

// This component fetches and displays all accounts.
// Users can click one account to open its details page.

import Link from "next/link";
import { useEffect, useState } from "react";

import { getAccounts } from "@/lib/api/accounts-api";
import type { Account } from "@/types/account";

export function AccountsList() {
  const [accounts, setAccounts] = useState<Account[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [errorMessage, setErrorMessage] = useState("");

  useEffect(() => {
    async function loadAccounts() {
      try {
        setIsLoading(true);
        setErrorMessage("");

        const data = await getAccounts();
        setAccounts(data);
      } catch (error) {
        setErrorMessage(
          error instanceof Error ? error.message : "Failed to load accounts."
        );
      } finally {
        setIsLoading(false);
      }
    }

    void loadAccounts();
  }, []);

  if (isLoading) {
    return <p>Loading accounts...</p>;
  }

  if (errorMessage) {
    return <p className="text-red-600">{errorMessage}</p>;
  }

  if (accounts.length === 0) {
    return <p>No accounts found.</p>;
  }

  return (
    <div className="space-y-4">
      {accounts.map((account) => (
        <Link
          key={account.id}
          href={`/accounts/${account.id}`}
          className="block rounded-xl border bg-white p-4 shadow-sm transition hover:shadow"
        >
          <div className="flex items-center justify-between gap-4">
            <div>
              <h2 className="text-lg font-semibold">{account.name}</h2>
              <p className="text-sm text-gray-600">
                {account.industry ?? "No industry"} •{" "}
                {account.company_size ?? "No company size"}
              </p>
            </div>

            <div className="text-right text-sm">
              <p>
                <span className="font-medium">Status:</span> {account.status}
              </p>
              <p>
                <span className="font-medium">Health:</span>{" "}
                {account.health_status ?? "N/A"}
              </p>
            </div>
          </div>
        </Link>
      ))}
    </div>
  );
}