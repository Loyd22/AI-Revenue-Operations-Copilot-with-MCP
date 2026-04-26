import type { Metadata } from "next";
import "./globals.css";

import { AuthProvider } from "@/lib/auth/auth-context";

export const metadata: Metadata = {
  title: "AI Revenue Operations Copilot",
  description: "Internal AI system for sales and revenue teams.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body>
        <AuthProvider>{children}</AuthProvider>
      </body>
    </html>
  );
}