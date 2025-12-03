"use client";

import { useEffect } from "react";
import { X, CheckCircle, XCircle } from "lucide-react";
import { cn } from "@/lib/utils";

interface NotificationProps {
  message: string;
  type: "success" | "error";
  onClose: () => void;
}

export default function Notification({ message, type, onClose }: NotificationProps) {
  useEffect(() => {
    const timer = setTimeout(() => {
      onClose();
    }, 5000);

    return () => clearTimeout(timer);
  }, [onClose]);

  return (
    <div
      className={cn(
        "fixed top-4 left-1/2 -translate-x-1/2 z-50 flex items-center gap-3 px-6 py-4 rounded-lg shadow-lg animate-in slide-in-from-top-5 max-w-md w-full",
        type === "success" ? "bg-green-50 border border-green-200" : "bg-red-50 border border-red-200"
      )}
    >
      {type === "success" ? (
        <CheckCircle className="w-5 h-5 text-green-600 flex-shrink-0" />
      ) : (
        <XCircle className="w-5 h-5 text-red-600 flex-shrink-0" />
      )}

      <p
        className={cn(
          "flex-1 text-sm font-medium",
          type === "success" ? "text-green-900" : "text-red-900"
        )}
      >
        {message}
      </p>

      <button
        onClick={onClose}
        className="flex-shrink-0 rounded-md p-1 hover:bg-gray-100 transition-colors"
      >
        <X className="w-4 h-4" />
      </button>
    </div>
  );
}
