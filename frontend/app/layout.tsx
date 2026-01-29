import type { ReactNode } from "react";
import "./globals.css";
import { AuthProvider } from "@/hooks/useAuth";

export default function RootLayout({
  children,
}: {
  children: ReactNode;
}) {
  return (
    <html lang="en">
      <AuthProvider>
        <body className="min-h-screen bg-background antialiased">
          {children}
        </body>
      </AuthProvider>
    </html>
  );
}