
import React from "react";
import type { User as UserType } from "@/types/user";
import Header from "./Header";

interface DashboardLayoutProps {
  user: UserType;
  children: React.ReactNode;
}

const DashboardLayout: React.FC<DashboardLayoutProps> = ({
  user,
  children,
}) => {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50">
      <Header user={user} />
      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        {children}
      </main>
    </div>
  );
};

export default DashboardLayout;
