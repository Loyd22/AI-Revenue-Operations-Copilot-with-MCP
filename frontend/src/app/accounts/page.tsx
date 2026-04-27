"use client";

// This page shows the list of accounts.
// It should only be visible to logged-in users.

import Link from "next/link";

import { AccountsList } from "@/features/accounts/components/accounts-list";
import { useAuth } from "@/lib/auth/auth-context";
import { useEffect } from "react";
import { useRouter } from "next/navigation";

export default function AccountsPage() {
  const router = useRouter();
  const { isAuthenticated, isLoading } = useAuth();

  useEffect(() => {
    if (!isLoading && !isAuthenticated) {
      router.replace("/login");
    }
  }, [isAuthenticated, isLoading, router]);

  if (isLoading) {
    return (
      <main className="min-h-screen flex items-center justify-center">
        <p>Loading...</p>
      </main>
    );
  }

  if (!isAuthenticated) {
    return null;
  }

  return (
    <main className="min-h-screen bg-gray-50 px-4 py-12">
      <div className="mx-auto max-w-5xl">
        <div className="mb-6 flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-semibold">Accounts</h1>
            <p className="text-sm text-gray-600">
              View and inspect customer accounts.
            </p>
          </div>

          <Link
            href="/dashboard"
            className="rounded-lg border px-4 py-2 text-sm"
          >
            Back to dashboard
          </Link>
        </div>

        <AccountsList />
      </div>
    </main>
  );
}