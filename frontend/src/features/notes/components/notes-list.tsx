"use client";

import { useEffect, useState } from "react";

import { getNotes } from "@/lib/api/notes-api";
import type { Note } from "@/types/note";

export function NotesList() {
  const [notes, setNotes] = useState<Note[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [errorMessage, setErrorMessage] = useState("");

  useEffect(() => {
    async function loadNotes() {
      try {
        setIsLoading(true);
        setErrorMessage("");
        const data = await getNotes();
        setNotes(data);
      } catch (error) {
        setErrorMessage(
          error instanceof Error ? error.message : "Failed to load notes."
        );
      } finally {
        setIsLoading(false);
      }
    }

    void loadNotes();
  }, []);

  if (isLoading) return <p>Loading notes...</p>;
  if (errorMessage) return <p className="text-red-600">{errorMessage}</p>;
  if (notes.length === 0) return <p>No notes found.</p>;

  return (
    <div className="space-y-4">
      {notes.map((note) => (
        <div key={note.id} className="rounded-xl border bg-white p-4 shadow-sm">
          <h2 className="text-lg font-semibold">{note.note_type}</h2>
          <p className="text-sm text-gray-600">
            Account ID: {note.account_id} • Deal ID: {note.deal_id ?? "N/A"}
          </p>
          <p className="mt-2 text-sm text-gray-700">{note.content}</p>
          <p className="mt-2 text-xs text-gray-500">Source: {note.source}</p>
        </div>
      ))}
    </div>
  );
}