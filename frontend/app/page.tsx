import { getCurrentUser } from "@/lib/auth";
import { redirect } from "next/navigation";
import LandingPage from "@/components/landing/LandingPage";

export default async function HomePage() {
  const user = await getCurrentUser();

  // Redirect to dashboard if already logged in
  if (user) {
    redirect("/dashboard");
  }

  return <LandingPage />;
}
