"use client";

interface MetricCardsProps {
  totalAccounts: number;
  totalDeals: number;
  totalActivities: number;
  totalNotes: number;
}

export function MetricCards({
  totalAccounts,
  totalDeals,
  totalActivities,
  totalNotes,
}: MetricCardsProps) {
  const items = [
    { label: "Total Accounts", value: totalAccounts },
    { label: "Total Deals", value: totalDeals },
    { label: "Total Activities", value: totalActivities },
    { label: "Total Notes", value: totalNotes },
  ];

  return (
    <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
      {items.map((item) => (
        <div key={item.label} className="rounded-xl border bg-white p-4 shadow-sm">
          <p className="text-sm text-gray-500">{item.label}</p>
          <p className="mt-2 text-2xl font-semibold">{item.value}</p>
        </div>
      ))}
    </div>
  );
}