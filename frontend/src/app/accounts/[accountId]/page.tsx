"use client";

// This page shows one account's details.
// It reads the accountId from the URL.

import Link from "next/link";
import { useParams, useRouter } from "next/navigation";
import { useEffect } from "react";

import { AccountDetails } from "@/features/accounts/components/account-details";
import { useAuth } from "@/lib/auth/auth-context";

export default function AccountDetailsPage() {
  const params = useParams();
  const router = useRouter();
  const { isAuthenticated, isLoading } = useAuth();

  const accountId = Number(params.accountId);

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

  if (Number.isNaN(accountId)) {
    return (
      <main className="min-h-screen flex items-center justify-center">
        <p>Invalid account ID.</p>
      </main>
    );
  }

  return (
    <main className="min-h-screen bg-gray-50 px-4 py-12">
      <div className="mx-auto max-w-5xl">
        <div className="mb-6">
          <Link
            href="/accounts"
            className="rounded-lg border px-4 py-2 text-sm inline-block"
          >
            Back to accounts
          </Link>
        </div>

        <AccountDetails accountId={accountId} />
      </div>
    </main>
  );
}