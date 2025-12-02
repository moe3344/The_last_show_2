import Link from "next/link";
import { Button } from "@/components/ui/button";

export default function NotFound() {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 p-4">
      <div className="text-center max-w-md">
        <h1 className="text-6xl font-bold text-white mb-4">404</h1>
        <h2 className="text-3xl font-bold text-white mb-4">Page Not Found</h2>
        <p className="text-purple-200 mb-6">
          The page you're looking for doesn't exist or has been moved.
        </p>
        <Link href="/">
          <Button className="bg-gradient-to-r from-purple-500 to-pink-500">
            Go Home
          </Button>
        </Link>
      </div>
    </div>
  );
}
