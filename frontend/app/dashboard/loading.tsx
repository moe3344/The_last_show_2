export default function DashboardLoading() {
  return (
    <div className="min-h-screen flex items-center justify-center">
      <div className="text-center">
        <div className="inline-block h-12 w-12 animate-spin rounded-full border-4 border-solid border-purple-500 border-r-transparent"></div>
        <p className="mt-4 text-muted-foreground">Loading dashboard...</p>
      </div>
    </div>
  );
}
