"use server";

import { FormState } from "@/types/auth";
import { cookies } from "next/headers";
import { redirect } from "next/navigation";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export async function login(
  prevState: FormState | undefined,
  formData: FormData
): Promise<FormState> {
  const email = formData.get("email") as string;
  const password = formData.get("password") as string;

  try {
    const response = await fetch(`${API_URL}/auth/login`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password }),
    });

    if (!response.ok) {
      const error = await response.json();
      return { error: error.detail || "Login failed" };
    }

    const data = await response.json();
    const cookieStore = await cookies();

    cookieStore.set("access_token", data.access_token, {
      httpOnly: true,
      secure: process.env.NODE_ENV === "production",
      sameSite: "lax",
      maxAge: 60 * 30, // 30 minutes (matches token expiration)
    });
  } catch (error) {
    return { error: "An unexpected error occurred" };
  }

  redirect("/dashboard");
}

export async function logout() {
  const cookieStore = await cookies();
  cookieStore.delete("access_token");
  redirect("/login");
}

export async function register(
  prevState: { error?: string } | undefined,
  formData: FormData
): Promise<{ error?: string }> {
  const email = formData.get("email") as string;
  const password = formData.get("password") as string;
  const fullName = formData.get("full_name") as string;

  try {
    const response = await fetch(`${API_URL}/auth/register`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password, full_name: fullName }),
    });

    if (!response.ok) {
      const error = await response.json();
      return { error: error.detail || "Registration failed" };
    }

    // Auto-login after registration
    const loginFormData = new FormData();
    loginFormData.append("email", email);
    loginFormData.append("password", password);

    // login() will redirect, so this will never return normally
    return await login(undefined, loginFormData);
  } catch (error) {
    // Re-throw redirect errors (Next.js uses them for navigation)
    if (error && typeof error === "object" && "digest" in error) {
      throw error;
    }
    return { error: "An unexpected error occurred" };
  }
}
