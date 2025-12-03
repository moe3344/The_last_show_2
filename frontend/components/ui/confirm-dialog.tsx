"use client";

import { Button } from "@/components/ui/button";
import { Dialog, DialogContent } from "@/components/ui/dialog";
import { AlertTriangle } from "lucide-react";

interface ConfirmDialogProps {
  open: boolean;
  title: string;
  message: string;
  onConfirm: () => void;
  onCancel: () => void;
}

export default function ConfirmDialog({
  open,
  title,
  message,
  onConfirm,
  onCancel,
}: ConfirmDialogProps) {
  return (
    <Dialog open={open} onOpenChange={onCancel}>
      <DialogContent onClose={onCancel}>
        <div className="p-6">
          <div className="flex items-start gap-4">
            <div className="flex-shrink-0">
              <AlertTriangle className="w-6 h-6 text-red-600" />
            </div>
            <div className="flex-1">
              <h3 className="text-lg font-semibold text-gray-900 mb-2">
                {title}
              </h3>
              <p className="text-sm text-gray-600">{message}</p>
            </div>
          </div>

          <div className="flex gap-3 mt-6 justify-end">
            <Button
              variant="outline"
              onClick={onCancel}
              className="px-4 py-2"
            >
              Cancel
            </Button>
            <Button
              onClick={onConfirm}
              className="px-4 py-2 bg-red-600 hover:bg-red-700"
            >
              Delete
            </Button>
          </div>
        </div>
      </DialogContent>
    </Dialog>
  );
}
