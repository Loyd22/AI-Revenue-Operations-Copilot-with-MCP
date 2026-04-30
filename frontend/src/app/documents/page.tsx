"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";

import { DocumentsList } from "@/features/documents/components/documents-list";
import { UploadDocumentForm } from "@/features/documents/components/upload-document-form";
import { useAuth } from "@/lib/auth/auth-context";

export default function DocumentsPage() {
  const router = useRouter();
  const { isAuthenticated, isLoading } = useAuth();
  const [refreshKey, setRefreshKey] = useState(0);

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
      <div className="mx-auto max-w-5xl space-y-6">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-semibold">Documents</h1>
            <p className="text-sm text-gray-600">
              Upload and inspect document metadata.
            </p>
          </div>

          <Link href="/dashboard" className="rounded-lg border px-4 py-2 text-sm">
            Back to dashboard
          </Link>
        </div>

        <UploadDocumentForm
          onUploaded={() => setRefreshKey((previous) => previous + 1)}
        />

        <DocumentsList refreshKey={refreshKey} />
      </div>
    </main>
  );
}