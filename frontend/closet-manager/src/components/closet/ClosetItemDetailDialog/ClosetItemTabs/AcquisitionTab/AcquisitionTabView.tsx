// ClosetManager/frontend/closet-manager/src/components/closet/ClosetItemDetailDialog/ClosetItemTabs/AcquisitionTab/AcquisitionTabView.tsx

import type { ClosetItem } from "../../../../../types/closet/closet-item";

interface AcquisitionTabViewProps {
  item: ClosetItem;
}

export const AcquisitionTabView = ({ item }: AcquisitionTabViewProps) => {
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-1">
          Date Acquired
        </label>
        <div className="p-2 bg-base-200 rounded">
          {item.dateAcquired
            ? new Date(item.dateAcquired).toLocaleDateString()
            : "Not set"}
        </div>
      </div>
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-1">
          Secondhand
        </label>
        <div className="p-2 bg-base-200 rounded">
          {item.secondhand ? "Yes" : "No"}
        </div>
      </div>
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-1">
          Purchase Price
        </label>
        <div className="p-2 bg-base-200 rounded">
          ${item.purchasePrice.toFixed(2)}
        </div>
      </div>
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-1">
          Original Price
        </label>
        <div className="p-2 bg-base-200 rounded">
          ${item.originalPrice.toFixed(2)}
        </div>
      </div>
      <div className="md:col-span-2">
        <label className="block text-sm font-medium text-gray-700 mb-1">
          Purchase Location
        </label>
        <div className="p-2 bg-base-200 rounded">{item.purchaseLocation}</div>
      </div>
      <div className="md:col-span-2">
        <label className="block text-sm font-medium text-gray-700 mb-1">
          Source
        </label>
        <div className="p-2 bg-base-200 rounded">{item.source}</div>
      </div>
    </div>
  );
};
