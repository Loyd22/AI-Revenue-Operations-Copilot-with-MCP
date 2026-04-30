"use client";

import { useState } from "react";

import { uploadDocument } from "@/lib/api/documents-api";

interface UploadDocumentFormProps {
  onUploaded: () => void;
}

export function UploadDocumentForm({ onUploaded }: UploadDocumentFormProps) {
  const [title, setTitle] = useState("");
  const [documentType, setDocumentType] = useState("policy");
  const [file, setFile] = useState<File | null>(null);

  const [isSubmitting, setIsSubmitting] = useState(false);
  const [errorMessage, setErrorMessage] = useState("");
  const [successMessage, setSuccessMessage] = useState("");

  async function handleSubmit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setErrorMessage("");
    setSuccessMessage("");

    if (!file) {
      setErrorMessage("Please choose a file.");
      return;
    }

    try {
      setIsSubmitting(true);
      await uploadDocument(title, documentType, file);

      setTitle("");
      setDocumentType("policy");
      setFile(null);
      setSuccessMessage("Document uploaded successfully.");
      onUploaded();
    } catch (error) {
      setErrorMessage(
        error instanceof Error ? error.message : "Upload failed."
      );
    } finally {
      setIsSubmitting(false);
    }
  }

  return (
    <form
      onSubmit={handleSubmit}
      className="rounded-xl border bg-white p-4 shadow-sm space-y-4"
    >
      <h2 className="text-lg font-semibold">Upload Document</h2>

      <div>
        <label className="mb-1 block text-sm font-medium">Title</label>
        <input
          type="text"
          className="w-full rounded-lg border px-3 py-2"
          value={title}
          onChange={(event) => setTitle(event.target.value)}
          placeholder="Document title"
          required
        />
      </div>

      <div>
        <label className="mb-1 block text-sm font-medium">Document Type</label>
        <select
          className="w-full rounded-lg border px-3 py-2"
          value={documentType}
          onChange={(event) => setDocumentType(event.target.value)}
        >
          <option value="policy">Policy</option>
          <option value="playbook">Playbook</option>
          <option value="process">Process</option>
          <option value="guide">Guide</option>
          <option value="other">Other</option>
        </select>
      </div>

      <div>
        <label className="mb-1 block text-sm font-medium">File</label>
        <input
          type="file"
          className="w-full rounded-lg border px-3 py-2"
          onChange={(event) => {
            const selectedFile = event.target.files?.[0] ?? null;
            setFile(selectedFile);
          }}
          required
        />
      </div>

      {errorMessage ? <p className="text-sm text-red-600">{errorMessage}</p> : null}
      {successMessage ? (
        <p className="text-sm text-green-600">{successMessage}</p>
      ) : null}

      <button
        type="submit"
        disabled={isSubmitting}
        className="rounded-lg bg-black px-4 py-2 text-white disabled:opacity-60"
      >
        {isSubmitting ? "Uploading..." : "Upload document"}
      </button>
    </form>
  );
}