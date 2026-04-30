"use client";

import { useEffect, useState } from "react";

import { getDocuments } from "@/lib/api/documents-api";
import type { DocumentItem } from "@/types/document";

interface DocumentsListProps {
  refreshKey?: number;
}

export function DocumentsList({ refreshKey = 0 }: DocumentsListProps) {
  const [documents, setDocuments] = useState<DocumentItem[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [errorMessage, setErrorMessage] = useState("");

  useEffect(() => {
    async function loadDocuments() {
      try {
        setIsLoading(true);
        setErrorMessage("");

        const data = await getDocuments();
        setDocuments(data);
      } catch (error) {
        setErrorMessage(
          error instanceof Error ? error.message : "Failed to load documents."
        );
      } finally {
        setIsLoading(false);
      }
    }

    void loadDocuments();
  }, [refreshKey]);

  if (isLoading) return <p>Loading documents...</p>;
  if (errorMessage) return <p className="text-red-600">{errorMessage}</p>;
  if (documents.length === 0) return <p>No documents found.</p>;

  return (
    <div className="space-y-4">
      {documents.map((document) => (
        <div key={document.id} className="rounded-xl border bg-white p-4 shadow-sm">
          <h2 className="text-lg font-semibold">{document.title}</h2>
          <p className="text-sm text-gray-600">
            {document.document_type} • {document.status}
          </p>
          <p className="mt-2 text-sm">File Name: {document.file_name}</p>
          <p className="text-sm break-all">Path: {document.storage_path}</p>
          <p className="text-sm">Uploaded By User ID: {document.uploaded_by_user_id ?? "N/A"}</p>
        </div>
      ))}
    </div>
  );
}