"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { Plus } from "lucide-react";

import { Button } from "@/components/ui/button";
import CreateObituaryForm from "@/components/CreateObituaryForm";
import DashboardLayout from "@/components/dashboard/DashboardLayout";
import ObituaryList from "@/components/dashboard/ObituaryList";
import Notification from "@/components/ui/notification";
import ConfirmDialog from "@/components/ui/confirm-dialog";
import type { Obituary } from "@/types/obituary";
import type { User as UserType } from "@/types/user";
import { getErrorMessage } from "@/types/errors";
import { deleteObituaryAction } from "@/app/actions/obituary";

interface DashboardClientProps {
  user: UserType;
  initialObituaries: Obituary[];
}

export default function DashboardClient({
  user,
  initialObituaries,
}: DashboardClientProps) {
  const [showCreateForm, setShowCreateForm] = useState(false);
  const [notification, setNotification] = useState<{
    message: string;
    type: "success" | "error";
  } | null>(null);
  const [deleteConfirm, setDeleteConfirm] = useState<string | null>(null);
  const router = useRouter();

  const handleDeleteObituary = async (id: string) => {
    setDeleteConfirm(id);
  };

  const confirmDelete = async () => {
    if (!deleteConfirm) return;

    const result = await deleteObituaryAction(deleteConfirm);
    setDeleteConfirm(null);

    if (result.success) {
      setNotification({
        message: "Obituary deleted successfully! ",
        type: "success",
      });
    } else {
      console.error("Failed to delete obituary:", result.error);
      setNotification({
        message: `Failed to delete obituary: ${result.error}`,
        type: "error",
      });
    }
  };

  const handleSuccess = () => {
    setShowCreateForm(false);
    setNotification({
      message: "Obituary created successfully!",
      type: "success",
    });
  };

  return (
    <>
      {notification && (
        <Notification
          message={notification.message}
          type={notification.type}
          onClose={() => setNotification(null)}
        />
      )}
      {deleteConfirm && (
        <ConfirmDialog
          title="Delete Obituary"
          message="Are you sure you want to delete this obituary? This action cannot be undone."
          onConfirm={confirmDelete}
          onCancel={() => setDeleteConfirm(null)}
        />
      )}
      <DashboardLayout user={user}>
        <div className="space-y-6">
          <div className="flex justify-between items-center">
            <div>
              <h2 className="text-3xl font-bold tracking-tight">Dashboard</h2>
              <p className="text-muted-foreground">
                Welcome back, {user.full_name}! 👋
              </p>
            </div>
            <Button
              onClick={() => setShowCreateForm(!showCreateForm)}
              className="flex items-center gap-2"
            >
              {showCreateForm ? "Cancel" : "Create Obituary"}
            </Button>
          </div>

          {showCreateForm && <CreateObituaryForm onSuccess={handleSuccess} />}

          <ObituaryList
            obituaries={initialObituaries}
            onDelete={handleDeleteObituary}
            onShowCreateForm={() => setShowCreateForm(true)}
            isFormShowing={showCreateForm}
          />
        </div>
      </DashboardLayout>
    </>
  );
}
