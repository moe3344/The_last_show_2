import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "The Last Show",
  description: "AI-powered obituary generator",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
