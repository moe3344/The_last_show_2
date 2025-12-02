"use client";

import { useEffect } from "react";
import { Button } from "@/components/ui/button";

export default function Error({
  error,
  reset,
}: {
  error: Error & { digest?: string };
  reset: () => void;
}) {
  useEffect(() => {
    console.error(error);
  }, [error]);

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 p-4">
      <div className="text-center max-w-md">
        <h2 className="text-3xl font-bold text-white mb-4">
          Something went wrong!
        </h2>
        <p className="text-purple-200 mb-6">
          We encountered an unexpected error. Please try again.
        </p>
        <Button
          onClick={reset}
          className="bg-gradient-to-r from-purple-500 to-pink-500"
        >
          Try again
        </Button>
      </div>
    </div>
  );
}
