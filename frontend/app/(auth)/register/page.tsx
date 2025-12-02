import { Metadata } from "next";
import Register from "@/components/auth/Register";

export const metadata: Metadata = {
  title: "Register | The Last Show",
  description: "Create an account to start generating AI-powered obituaries",
};

export default function RegisterPage() {
  return <Register />;
}
