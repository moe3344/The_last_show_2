import { Metadata } from "next";
import Login from "@/components/auth/Login";

export const metadata: Metadata = {
  title: "Login | The Last Show",
  description: "Sign in to your account to create and manage obituaries",
};

export default function LoginPage() {
  return <Login />;
}
