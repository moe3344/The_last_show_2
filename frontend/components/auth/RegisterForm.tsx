"use client";

import { useActionState } from "react";
import { useFormStatus } from "react-dom";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Button } from "@/components/ui/button";

interface RegisterFormProps {
  registerAction: (
    prevState: { error?: string } | undefined,
    formData: FormData
  ) => Promise<{ error?: string }>;
}

function SubmitButton() {
  const { pending } = useFormStatus();

  return (
    <Button type="submit" className="w-full" disabled={pending}>
      {pending ? "Creating account..." : "Create Account"}
    </Button>
  );
}

export default function RegisterForm({ registerAction }: RegisterFormProps) {
  const [state, formAction] = useActionState(registerAction, {} as { error?: string });

  return (
    <form action={formAction} className="space-y-6">
      {state?.error && (
        <div className="bg-red-50 text-red-600 p-3 rounded-md text-sm">
          {state.error}
        </div>
      )}

      <div className="space-y-2">
        <Label htmlFor="full_name" className="text-white">
          Full Name
        </Label>
        <Input
          id="full_name"
          name="full_name"
          type="text"
          required
          placeholder="John Doe"
          className="bg-white/20 border-white/30 text-white placeholder:text-white/50"
        />
      </div>

      <div className="space-y-2">
        <Label htmlFor="email" className="text-white">
          Email
        </Label>
        <Input
          id="email"
          name="email"
          type="email"
          required
          placeholder="you@example.com"
          className="bg-white/20 border-white/30 text-white placeholder:text-white/50"
        />
      </div>

      <div className="space-y-2">
        <Label htmlFor="password" className="text-white">
          Password
        </Label>
        <Input
          id="password"
          name="password"
          type="password"
          required
          placeholder="••••••••"
          minLength={6}
          className="bg-white/20 border-white/30 text-white placeholder:text-white/50"
        />
      </div>

      <SubmitButton />
    </form>
  );
}
