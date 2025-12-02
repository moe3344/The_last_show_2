import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";

export function proxy(request: NextRequest) {
  const token = request.cookies.get("access_token");
  const { pathname } = request.nextUrl;

  // Public routes that don't need auth
  const publicRoutes = ["/", "/login", "/register"];
  const isPublicRoute = publicRoutes.includes(pathname);

  // Redirect to login if not authenticated and trying to access protected route
  if (!token && !isPublicRoute) {
    return NextResponse.redirect(new URL("/login", request.url));
  }

  // Redirect to dashboard if authenticated and trying to access login/register
  if (token && (pathname === "/login" || pathname === "/register")) {
    return NextResponse.redirect(new URL("/dashboard", request.url));
  }

  return NextResponse.next();
}

export const config = {
  matcher: ["/((?!api|_next/static|_next/image|favicon.ico).*)"],
};
