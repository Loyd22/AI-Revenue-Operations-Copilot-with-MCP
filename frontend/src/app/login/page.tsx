import Link from "next/link";

import { PublicRoute } from "@/components/guards/public-route";
import { LoginForm } from "@/features/auth/components/login-form";

export default function LoginPage() {
  return (
    <PublicRoute>
      <main className="min-h-screen bg-gray-50 px-4 py-12">
        <div className="mx-auto max-w-md rounded-2xl bg-white p-8 shadow-sm">
          <h1 className="text-2xl font-semibold">Sign in</h1>
          <p className="mt-2 text-sm text-gray-600">
            Access your AI Revenue Operations Copilot workspace.
          </p>

          <div className="mt-6">
            <LoginForm />
          </div>

          <p className="mt-6 text-sm text-gray-600">
            Do not have an account?{" "}
            <Link href="/signup" className="font-medium text-black underline">
              Sign up
            </Link>
          </p>
        </div>
      </main>
    </PublicRoute>
  );
}