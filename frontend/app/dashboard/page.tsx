import { Metadata } from "next";
import { getCurrentUser } from "@/lib/auth";
import { redirect } from "next/navigation";
import DashboardClient from "@/components/DashboardClient";
import { serverAPI } from "@/lib/server-api";

export const metadata: Metadata = {
  title: "Dashboard | The Last Show",
  description: "Manage your obituaries and create new ones",
};

export default async function DashboardPage() {
  const user = await getCurrentUser();

  if (!user) {
    redirect("/login");
  }

  // Correctly call the renamed function and destructure the response
  const response = await serverAPI.getMyObituaries();

  return (
    <DashboardClient user={user} initialObituaries={response.obituaries} />
  );
}
