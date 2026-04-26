"use client";

// This temporary homepage helps us test whether auth is working.
// Later, this page will become the real dashboard or redirect logic.

import Link from "next/link";

import { useAuth } from "@/lib/auth/auth-context";

export default function HomePage() {
  const { user, isAuthenticated, isLoading, logout } = useAuth();

  if (isLoading) {
    return (
      <main className="min-h-screen flex items-center justify-center">
        <p>Loading...</p>
      </main>
    );
  }

  return (
    <main className="min-h-screen bg-gray-50 px-4 py-12">
      <div className="mx-auto max-w-2xl rounded-2xl bg-white p-8 shadow-sm">
        <h1 className="text-2xl font-semibold">
          AI Revenue Operations Copilot with MCP
        </h1>

        <div className="mt-6">
          {isAuthenticated && user ? (
            <div className="space-y-4">
              <p className="text-green-700">You are logged in.</p>

              <div className="rounded-xl border p-4">
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

              <button
                onClick={logout}
                className="rounded-lg bg-black px-4 py-2 text-white"
              >
                Logout
              </button>
            </div>
          ) : (
            <div className="space-y-4">
              <p>You are not logged in.</p>

              <div className="flex gap-3">
                <Link
                  href="/login"
                  className="rounded-lg bg-black px-4 py-2 text-white"
                >
                  Go to login
                </Link>

                <Link
                  href="/signup"
                  className="rounded-lg border px-4 py-2"
                >
                  Go to signup
                </Link>
              </div>
            </div>
          )}
        </div>
      </div>
    </main>
  );
}