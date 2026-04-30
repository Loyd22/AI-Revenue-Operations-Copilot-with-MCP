"use client";

interface RecentSectionProps<T> {
  title: string;
  items: T[];
  renderItem: (item: T) => React.ReactNode;
}

export function RecentSection<T>({
  title,
  items,
  renderItem,
}: RecentSectionProps<T>) {
  return (
    <div className="rounded-xl border bg-white p-4 shadow-sm">
      <h2 className="text-lg font-semibold">{title}</h2>

      <div className="mt-4 space-y-3">
        {items.length === 0 ? (
          <p className="text-sm text-gray-500">No data found.</p>
        ) : (
          items.map((item, index) => (
            <div key={index} className="rounded-lg border p-3">
              {renderItem(item)}
            </div>
          ))
        )}
      </div>
    </div>
  );
}