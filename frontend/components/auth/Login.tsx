
import { login } from "@/app/actions/auth";
import LoginForm from "@/components/auth/LoginForm";
import Link from "next/link";

export default function Login() {
  return (
    <div
      className="min-h-screen flex items-center justify-center bg-gradient-to-br from-slate-900 via-purple-900
  to-slate-900 p-4"
    >
      <div className="w-full max-w-md">
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-white mb-2">Welcome Back</h1>
          <p className="text-purple-200">Sign in to your account</p>
        </div>

        <div className="bg-white/10 backdrop-blur-lg rounded-xl p-8 border border-white/20">
          <LoginForm loginAction={login} />

          <div className="mt-6 text-center">
            <p className="text-purple-200">
              Don&apos;t have an account?{" "}
              <Link
                href="/register"
                className="text-white font-semibold hover:underline"
              >
                Sign up
              </Link>
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
