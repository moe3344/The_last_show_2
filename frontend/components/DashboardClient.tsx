"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { Plus } from "lucide-react";

import { Button } from "@/components/ui/button";
import CreateObituaryForm from "@/components/CreateObituaryForm";
import DashboardLayout from "@/components/dashboard/DashboardLayout";
import ObituaryList from "@/components/dashboard/ObituaryList";
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
  const router = useRouter();

  const handleDeleteObituary = async (id: string) => {
    if (!confirm("Are you sure you want to delete this obituary?")) {
      return;
    }

    const result = await deleteObituaryAction(id);

    if (result.success) {
      // Refresh the page to get the updated list of obituaries from the server
      // router.refresh(); // DIAGNOSTIC: Temporarily disabled
      alert("Obituary deleted. Please refresh the page to see the update.");
    } else {
      console.error("Failed to delete obituary:", result.error);
      alert(`Failed to delete obituary: ${result.error}`);
    }
  };

  const handleSuccess = () => {
    setShowCreateForm(false);
    // router.refresh(); // DIAGNOSTIC: Temporarily disabled
    alert("Obituary created. Please refresh the page to see the update.");
  };

  return (
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
            <Plus className="w-4 h-4" />
            {showCreateForm ? "Cancel" : "Create Obituary"}
          </Button>
        </div>

        {showCreateForm && <CreateObituaryForm onSuccess={handleSuccess} />}

        <ObituaryList
          obituaries={initialObituaries}
          onDelete={handleDeleteObituary}
          onShowCreateForm={() => setShowCreateForm(true)}
        />
      </div>
    </DashboardLayout>
  );
}
