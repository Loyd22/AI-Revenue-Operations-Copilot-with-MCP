"use client";

// This component fetches and displays one account by ID.

import { useEffect, useState } from "react";

import { getAccountById } from "@/lib/api/accounts-api";
import type { Account } from "@/types/account";

interface AccountDetailsProps {
  accountId: number;
}

export function AccountDetails({ accountId }: AccountDetailsProps) {
  const [account, setAccount] = useState<Account | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [errorMessage, setErrorMessage] = useState("");

  useEffect(() => {
    async function loadAccount() {
      try {
        setIsLoading(true);
        setErrorMessage("");

        const data = await getAccountById(accountId);
        setAccount(data);
      } catch (error) {
        setErrorMessage(
          error instanceof Error ? error.message : "Failed to load account."
        );
      } finally {
        setIsLoading(false);
      }
    }

    void loadAccount();
  }, [accountId]);

  if (isLoading) {
    return <p>Loading account...</p>;
  }

  if (errorMessage) {
    return <p className="text-red-600">{errorMessage}</p>;
  }

  if (!account) {
    return <p>Account not found.</p>;
  }

  return (
    <div className="rounded-2xl bg-white p-8 shadow-sm">
      <h1 className="text-2xl font-semibold">{account.name}</h1>

      <div className="mt-6 grid gap-4 sm:grid-cols-2">
        <div className="rounded-xl border p-4">
          <p className="text-sm text-gray-500">Industry</p>
          <p className="font-medium">{account.industry ?? "N/A"}</p>
        </div>

        <div className="rounded-xl border p-4">
          <p className="text-sm text-gray-500">Company Size</p>
          <p className="font-medium">{account.company_size ?? "N/A"}</p>
        </div>

        <div className="rounded-xl border p-4">
          <p className="text-sm text-gray-500">Status</p>
          <p className="font-medium">{account.status}</p>
        </div>

        <div className="rounded-xl border p-4">
          <p className="text-sm text-gray-500">Health Status</p>
          <p className="font-medium">{account.health_status ?? "N/A"}</p>
        </div>

        <div className="rounded-xl border p-4">
          <p className="text-sm text-gray-500">Renewal Date</p>
          <p className="font-medium">{account.renewal_date ?? "N/A"}</p>
        </div>

        <div className="rounded-xl border p-4">
          <p className="text-sm text-gray-500">Owner User ID</p>
          <p className="font-medium">{account.owner_user_id ?? "N/A"}</p>
        </div>
      </div>
    </div>
  );
}