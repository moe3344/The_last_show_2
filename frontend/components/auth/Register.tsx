
import { register } from "@/app/actions/auth";
import RegisterForm from "@/components/auth/RegisterForm";
import Link from "next/link";

export default function Register() {
  return (
    <div
      className="min-h-screen flex items-center justify-center bg-gradient-to-br from-slate-900 via-purple-900
  to-slate-900 p-4"
    >
      <div className="w-full max-w-md">
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-white mb-2">Create Account</h1>
          <p className="text-purple-200">Start creating beautiful obituaries</p>
        </div>

        <div className="bg-white/10 backdrop-blur-lg rounded-xl p-8 border border-white/20">
          <RegisterForm registerAction={register} />

          <div className="mt-6 text-center">
            <p className="text-purple-200">
              Already have an account?{" "}
              <Link
                href="/login"
                className="text-white font-semibold hover:underline"
              >
                Sign in
              </Link>
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
