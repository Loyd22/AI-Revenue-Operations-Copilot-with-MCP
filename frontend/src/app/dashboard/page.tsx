"use client";

// This dashboard page checks auth directly.
// This avoids the extra wrapper that is currently getting stuck.

import { useEffect } from "react";
import { useRouter } from "next/navigation";

import { useAuth } from "@/lib/auth/auth-context";

export default function DashboardPage() {
  const router = useRouter();
  const { user, logout, isAuthenticated, isLoading } = useAuth();

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
      <div className="mx-auto max-w-3xl rounded-2xl bg-white p-8 shadow-sm">
        <h1 className="text-2xl font-semibold">Dashboard</h1>
        <p className="mt-2 text-gray-600">
          Welcome to the AI Revenue Operations Copilot dashboard.
        </p>

        {user ? (
          <div className="mt-6 rounded-xl border p-4 space-y-2">
            <p>
              <span className="font-medium">Name:</span> {user.full_name}
            </p>
            <p>
              <span className="font-medium">Email:</span> {user.email}
            </p>
            <p>
              <span className="font-medium">Role:</span> {user.role}
            </p>
          </div>
        ) : (
          <p className="mt-6">No user data found.</p>
        )}

        <div className="mt-6">
          <button
            onClick={logout}
            className="rounded-lg bg-black px-4 py-2 text-white"
          >
            Logout
          </button>
        </div>
      </div>
    </main>
  );
}