"use client";

import Link from "next/link";
import { useParams, useRouter } from "next/navigation";
import { useEffect } from "react";

import { DealDetails } from "@/features/deals/components/deal-details";
import { useAuth } from "@/lib/auth/auth-context";

export default function DealDetailsPage() {
  const params = useParams();
  const router = useRouter();
  const { isAuthenticated, isLoading } = useAuth();

  const dealId = Number(params.dealId);

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

  if (Number.isNaN(dealId)) {
    return (
      <main className="min-h-screen flex items-center justify-center">
        <p>Invalid deal ID.</p>
      </main>
    );
  }

  return (
    <main className="min-h-screen bg-gray-50 px-4 py-12">
      <div className="mx-auto max-w-5xl">
        <div className="mb-6">
          <Link
            href="/deals"
            className="inline-block rounded-lg border px-4 py-2 text-sm"
          >
            Back to deals
          </Link>
        </div>

        <DealDetails dealId={dealId} />
      </div>
    </main>
  );
}